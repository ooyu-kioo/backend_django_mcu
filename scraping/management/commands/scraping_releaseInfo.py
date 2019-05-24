import json
from django.core.management.base import BaseCommand, CommandError

# chromedriver
import chromedriver_binary
# seleniumを動かすドライバ
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options


# ファイルを単体実行とmanage.py両方から実行できるよう、main()関数に処理を書いてclass commandに入れてやる
def main():
    print("----- custom command [scraping_releaseInfo] start -----")

    # driver設定
    options = Options()
    # heroku用に指定
    options.binary_location = '/app/.apt/usr/bin/google-chrome'
    options.add_argument('--headless')  # chrome driverをheadlessモードで起動

    # driverインスタンス作成
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(20)  # 待機時間設定

    # jsonファイル読み込み(withを付けるとブロック抜けた時に自動でファイルをclose()してくれる)
    # manage.pyからの起動なので、そこからの相対パス
    with open("./scraping/management/commands/scraping_list.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    ########################################
    # scraping(data_key＝アーティスト分繰り返す)
    ########################################
    artist_names = []
    release_titles = []
    release_dates = []
    buy_urls = []

    urls = ["https://www.oricon.co.jp/release/single/", "https://www.oricon.co.jp/release/album/",
            "https://www.oricon.co.jp/release/dvd/", "https://www.oricon.co.jp/release/blu-ray/"]

    # single, album, dvd, bluelay情報取得
    for url in urls:
        page = 1
        driver.get(url)  # urlページを開く

        while len(driver.find_elements_by_link_text('次週')) > 0:

            print(f'page：{page}')
            page += 1

            def get_release_info():
                get_artistNames = driver.find_elements_by_class_name(
                    "artist")  # artist名
                get_releaseTitles = driver.find_elements_by_class_name(
                    "title")  # タイトル
                get_releaseDates = driver.find_elements_by_class_name(
                    "cell-date")  # 発売日
                get_buyUrl = driver.find_elements_by_css_selector(
                    "div.box-buy-music > ul > li > a")  # Amazon URL

                for data_key in data:  # jsonのartistそれぞれに対して
                    for i in range(len(get_artistNames)):  # 取得したartist照合
                        if data_key == get_artistNames[i].text:  # 一致するなら格納
                            artist_names.append(get_artistNames[i].text)
                            release_titles.append(get_releaseTitles[i].text)
                            release_dates.append(get_releaseDates[i].text)
                            buy_urls.append(
                                get_buyUrl[i].get_attribute('href'))

            get_release_info()

            try:  # 画面遷移
                driver.find_element_by_link_text('次週').click()
            except:
                pass

        get_release_info()  # 最後の１ページスクレイピング

        # 配列リバース
        artist_names.reverse()
        release_titles.reverse()
        release_dates.reverse()
        buy_urls.reverse()

        print(artist_names)
        print(release_titles)
        print(release_dates)
        print(buy_urls)

    # -------
    # DB格納
    # -------
    # 外部ファイルがdjangoのmodelを使用する場合、djangoのsetupが必要
    import os
    import django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                          "django_vue_mcu.settings")
    django.setup()  # (引数１の環境変数が引数２を指定するよう設定)

    from scraping.models import ReleaseInfo  # ReleaseInfoテーブルをインポート

    # object生成
    for artist_name, release_title, release_date, buy_url in zip(artist_names, release_titles, release_dates, buy_urls):
        try:  # id, created_at はdefault設定してるので自動で入る
            ReleaseInfo.objects.create(
                artist_name=artist_name, release_title=release_title, release_date=release_date, buy_url=buy_url)  # ReleaseInfoオブジェクト作成
        except:
            print(f"unique_error. release_title：{release_title}")  # 一意性エラー
            pass

    # ドライバー終了
    driver.quit()

    # 表示(エラースルー)
    print("")
    print(ReleaseInfo.objects.all())
    print("")
    print("----- custom command [scraping_releaseInfo] end -----")


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()


if __name__ == '__main__':
    main()
