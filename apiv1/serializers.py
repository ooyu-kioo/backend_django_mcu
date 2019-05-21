#
# modelオブジェクトとJSON文字列の相互変換・入力データのvalidation：
#

from rest_framework import serializers
from scraping.models import Infomation


# Infomationモデルに対するserializer
class InfomationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Infomation  # 使用するmodel指定
        fields = ("id", "artist_name", "info_title",
                  "info_body_link", "created_at")  # APIで返す使用するカラムを指定

# 複数のmodelを扱う場合
# class InfomationListSerializer(serializers.ListSerializer)
