#
# artistinfoをscraping・label付け
#

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

# NLP
import copy
import numpy as np
import nagisa  # 形態素解析
import neologdn  # テキストの正規化
import jctconv  # 半角文字 => 全角文字
import re  # 正規表現
import joblib  # model保存
# 複数回出現する単語=分析に役立たない単語を見つけ出す
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier


# ファイルを単体実行とmanage.py両方から実行できるよう、main()関数に処理を書いてclass commandに入れてやる
def main():
    print("----- custom command [scraping] start -----")

    # osの環境変数を取得
    # os.environ()

    # driver設定
    options = Options()

    # Heroku用設定(pathが設定されている場合)
    # if CHROME_BINARY_LOCATION:
    # options.binary_location = CHROME_BINARY_LOCATION
    options.binary_location = '/app/.apt/usr/bin/google-chrome'

    options.add_argument('--headless')  # chrome driverをheadlessモードで起動

    # driverインスタンス作成
    # if CHROME_BINARY_LOCATION: # Heroku用設定
    driver = webdriver.Chrome(options=options)
    # else:
    # driver = webdriver.Chrome(options=options)

    driver.implicitly_wait(20)  # 待機時間設定

    # jsonファイル読み込み(withを付けるとブロック抜けた時に自動でファイルをclose()してくれる)
    # manage.pyからの起動なので、そこからの相対パス
    with open("./scraping/management/commands/scraping_list.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    ##########################################
    # scraping(data_key＝アーティスト分繰り返す)
    ##########################################
    for data_key in data:

        url = data[data_key]["URL"]  # アクセスURL(infoに直とび)
        driver.get(url)  # urlページを開く

        # --------------------
        # infoTitleの取得(sony)
        # --------------------

        # 配列初期化
        get_infoTitles = []  # element格納用
        infoTitles = []  # 要素格納用
        # タグ情報取得
        if data[data_key]["info_title_get"] == "class":  # 取得方法：class
            get_infoTitles = driver.find_elements_by_class_name(
                data[data_key]["info_title_el"])

        # タイトル配列格納
        for i in range(len(get_infoTitles)):
            item = get_infoTitles[i]
            print(item.text)
            infoTitles.append(item.text)
        # 配列をリバース
        infoTitles.reverse()

        # --------------------
        # infoLinkの取得(sony)
        # --------------------

        # 配列初期化
        get_infoLinks = []
        infoLinks = []
        # タグ情報取得
        if data[data_key]["info_body_get"] == "css":  # 取得方法：CSS
            get_infoLinks = driver.find_elements_by_css_selector(
                data[data_key]["info_body_el"])

        # リンク配列格納
        for i in range(len(get_infoLinks)):
            item = get_infoLinks[i]
            print(item.get_attribute('href'))
            infoLinks.append(item.get_attribute("href"))
        # 配列リバース
        infoLinks.reverse()

        # ---------------
        # infoのlabel付け
        # ---------------
        text_list = copy.deepcopy(infoTitles)
        nagisa_list = np.array([])
        new_tagger = nagisa.Tagger(
            single_word_list=["凛として時雨", "ピエール中野", "tk from 凛として時雨"])  # ユーザー辞書定義

        for item in text_list:
            # 前処理
            item = item.lower()  # アルファベット大文字 => 小文字へ変換
            item = neologdn.normalize(item)  # 無駄なスペースなどを排除
            item = jctconv.h2z(item)  # 半角文字 => 全角文字に変換
            item = re.sub(r'\d+', '', item)  # 数字を空文字に変換

            # 形態素解析
            words = new_tagger.extract(item, extract_postags=['名詞'])  # 名詞のみ抽出
            words = ' '.join(words.words)  # wordsの配列要素を半角スペースで結合
            nagisa_list = np.append(nagisa_list, words)

        # インスタンス生成(※vocabulary＝model作成時に使用したコーパス(使用しないとmodelと入力データの次元が一致しない))
        vocabulary = joblib.load(
            './scraping/management/commands/mcu_vocabulary.jb')
        vectorizer = TfidfVectorizer(vocabulary=vocabulary, token_pattern='(?u)\\b\\w+\\b', stop_words=[
                                     "凛として時雨", "ピエール田中", "ヨルシカ", "uverworld", "topics", "alexandros"])
        # ベクトル化
        tfidf = vectorizer.fit_transform(nagisa_list)  # 引数は分かち書きされたlist
        label_text = tfidf.toarray()

        # 予測
        rfc = joblib.load("mcu_randomForest.jb")
        pred = rfc.predict(label_text)
        pred_labels = pred.tolist()

        # label変換
        text_label = {1: "release", 2: "live", 3: "media", 4: "other"}
        for i, item in enumerate(pred_labels, 0):
            if item in text_label:
                pred_labels[i] = text_label[item]
            else:
                pred_labels[i] = text_label[4]

        # -------
        # DB格納
        # -------

        # 外部ファイルがdjangoのmodelを使用する場合、djangoのsetupが必要
        import os
        import django
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "django_vue_mcu.settings")
        django.setup()  # (引数１の環境変数が引数２を指定するよう設定)

        from scraping.models import Infomation  # Infomationテーブルをインポート

        # Infomationオブジェクト登録
        artist_name = data_key
        for info_title, info_body_link, info_label in zip(infoTitles, infoLinks, pred_labels):
            try:  # id, created_at はdefault設定してるので自動で入る
                Infomation.objects.create(
                    artist_name=artist_name, info_title=info_title, info_body_link=info_body_link, info_label=info_label)
            except:
                print(f"unique_error. infoTitle： {infoTitle}")  # 一意性エラー
                pass

        # もしくは
        # obj = Infomation(artist_name = , info_title = )
        # obj.save()

    driver.quit()
    print("----- custom command [scraping] end -----")


class Command(BaseCommand):
    def handle(self, *args, **options):
        main()


if __name__ == '__main__':
    main()
