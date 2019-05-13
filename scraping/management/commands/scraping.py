# TODO 機能
#     ・PWA化(既存のwebappをやった時の影響)
#     ・PWA・通知：最初は新着を全部通知でいいか
#     ・言語処理：タグ付け(pwaの通知のため)
#     ・リリース情報取得 or info言語処理？ 普通にdiscograpyから取ってきた方が楽そう
#     ・データの表示順序おかしく無い？どこに原因？
#       配列でinfoを上から取得 => db格納時に自動でcreated_at設定(default)：格納は配列の最初から = infoの上の情報が古いcreateになる
#       => ・格納の順番を変えてやる：格納前の配列をリバースする  ・1h間隔くらいなら同時取得も少ないから情報溜まってくのを待つ

# TODO その他
#     ・クロールリストjsonのimport > 相対パス、ファイル名で指定できない？
#     ・一部のinfo__bodyの表示どうする？

# import os
import time
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
    print("----- custom command [scraping] start -----")

    # osの環境変数を取得
    # os.environ()

    # driver設定
    options= Options()
    
    # Heroku用設定(pathが設定されている場合)
    # if CHROME_BINARY_LOCATION:
    # options.binary_location = CHROME_BINARY_LOCATION
    options.binary_location = '/app/.apt/usr/bin/google-chrome'
    
    options.add_argument('--headless') # chrome driverをheadlessモードで起動

    # driverインスタンス作成
    # if CHROME_BINARY_LOCATION: # Heroku用設定
    driver = webdriver.Chrome(options=options)
    # else: 
        # driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(20) # 待機時間設定

    # jsonファイル読み込み(withを付けるとブロック抜けた時に自動でファイルをclose()してくれる)
    # manage.pyからの起動なので、そこからの相対パス
    with open("./scraping/management/commands/scraping_list.json", "r", encoding = "utf-8") as f:
        data = json.load(f)

    ########################################
    # scraping(data_key＝アーティスト分繰り返す)
    ########################################
    for data_key in data:

        url= data[data_key]["URL"] # アクセスURL(infoに直とび)
        driver.get(url) # urlページを開く

        #--------------------
        # infoTitleの取得(sony)
        #--------------------

        # 配列初期化
        get_infoTitles = [] # element格納用
        infoTitles     = [] # 要素格納用
        # タグ情報取得
        if data[data_key]["info_title_get"] == "class": # 取得方法：class
            get_infoTitles = driver.find_elements_by_class_name(data[data_key]["info_title_el"])


        # タイトル配列格納
        for i in range(len(get_infoTitles)):
            item = get_infoTitles[i]
            print(item.text)
            infoTitles.append(item.text)
        print("")
        # 配列をリバース
        infoTitles.reverse()


        #--------------------
        # infoLinkの取得(sony)
        #--------------------
        
        # 配列初期化
        get_infoLinks = []
        infoLinks     = []
        # タグ情報取得
        if data[data_key]["info_body_get"] == "css": # 取得方法：CSS
            get_infoLinks = driver.find_elements_by_css_selector(data[data_key]["info_body_el"])

        # リンク配列格納
        for i in range(len(get_infoLinks)):
            item = get_infoLinks[i]
            print(item.get_attribute('href'))
            infoLinks.append(item.get_attribute("href"))
        print("")
        # 配列リバース
        infoLinks.reverse()


        #-------
        # DB格納
        #-------

        # 外部ファイルがdjangoのmodelを使用する場合、djangoのsetupが必要
        import os
        import django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_vue_mcu.settings")
        django.setup() # (引数１の環境変数が引数２を指定するよう設定)

        from scraping.models import Infomation # Infomationテーブルをインポート

        # test インスタンス生成、save これだと何か上手くいかない
        # test = Infomation()
        # test.artist_name = artistName
        # test.info_title = infoTitle
        # test.save

        # DB格納用変数
        artist_name = data_key
        info_title = ""
        info_body_link = ""

        # title,link設定
        print("")
        for infoTitle, infoLink in zip(infoTitles, infoLinks):
            info_title = infoTitle
            info_body_link = infoLink
            try: # id, created_at はdefault設定してるので自動で入る
                Infomation.objects.create(artist_name = artist_name, info_title = info_title, info_body_link = info_body_link) # Infomationオブジェクト作成
            except:
                print(f"unique_error. infoTitle： {infoTitle}") # 一意性エラー
                pass
        print("")
        # もしくは
        # obj = Infomation(artist_name = , info_title = )
        # obj.save()

# ------------------------------------------------------------------------

    # ドライバー終了
    driver.quit()

    # 表示(エラースルー)
    print("")
    print(Infomation.objects.all())
    print("")
    print("----- custom command [scraping] end -----")



class Command(BaseCommand):
    def handle(self, *args, **options):
        main()

if __name__ == '__main__':
    main()