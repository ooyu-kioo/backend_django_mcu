#
# JSON形式のレスポンスオブジェクトの作成：
#
from rest_framework import viewsets, routers
from scraping.models import Infomation
from scraping.models import ReleaseInfo
from .serializers import InfomationSerializer
from .serializers import ReleaseInfoSerializer


class InfomationViewSet(viewsets.ReadOnlyModelViewSet):  # 情報を参照するだけなのでReadOnly
    # Infomationモデルの一覧GET,詳細GETを行うAPI
    # modelにDB操作のqueryを送る(filterかけて一部を取り出すとかできる)
    queryset = Infomation.objects.all().order_by("created_at").reverse()[0:30]
    serializer_class = InfomationSerializer  # serializeするクラスを指定

    # Infomation.objects.order_by(“-created_at”)[0:100] # 作成日順に先頭100件
    # reverse()


class ReleaseInfoViewSet(viewsets.ReadOnlyModelViewSet):
    # ReleaseInfoモデルの一覧GET,詳細GETを行うAPI
    queryset = ReleaseInfo.objects.all().order_by("created_at").reverse()[0:30]
    serializer_class = ReleaseInfoSerializer
