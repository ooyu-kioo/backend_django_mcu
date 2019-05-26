#
# JSON形式のレスポンスオブジェクトの作成：
#

from datetime import datetime

from rest_framework import viewsets, routers
from scraping.models import Infomation
from scraping.models import ReleaseInfo
from .serializers import InfomationSerializer
from .serializers import ReleaseInfoSerializer


class InfomationViewSet(viewsets.ReadOnlyModelViewSet):  # 情報を参照するだけなのでReadOnly
    # Infomationモデルの一覧GET,詳細GETを行うAPI
    # modelにDB操作のqueryを送る(filterかけて一部を取り出すとかできる)
    queryset = Infomation.objects.all().order_by("created_at").reverse()

    # created_atをxxxx年yy月zz日に変換
    for query in queryset:
        query.created_at = query.created_at.date()

    serializer_class = InfomationSerializer  # serializeするクラスを指定

    # Infomation.objects.order_by(“-created_at”)[0:100] # 作成日順に先頭100件
    # reverse()


class ReleaseInfoViewSet(viewsets.ReadOnlyModelViewSet):
    # ReleaseInfoモデルの一覧GET,詳細GETを行うAPI
    queryset = ReleaseInfo.objects.all().order_by("created_at").reverse()
    serializer_class = ReleaseInfoSerializer
