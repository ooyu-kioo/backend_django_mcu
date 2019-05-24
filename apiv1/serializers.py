#
# modelオブジェクトとJSON文字列の相互変換・入力データのvalidation：
#

from rest_framework import serializers
from scraping.models import Infomation
from scraping.models import ReleaseInfo


# Infomationモデルに対するserializer
class InfomationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Infomation  # 使用するmodel指定
        fields = ("id", "artist_name", "info_title",
                  "info_body_link", "created_at")  # APIで返す使用するカラムを指定


# 一度に複数のmodelを扱う(API上で)訳ではないから単一のserializerでいい？
class ReleaseInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReleaseInfo
        fields = ("id", "artist_name", "release_title",
                  "release_date", "buy_url", "created_at")

# 複数のmodelを扱う場合
# class InfomationListSerializer(serializers.ListSerializer)
