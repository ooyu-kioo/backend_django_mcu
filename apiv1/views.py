#
# JSON形式のレスポンスオブジェクトの作成：
#

from rest_framework import viewsets, routers
from scraping.models import Infomation
from .serializers import InfomationSerializer

class InfomationViewSet(viewsets.ReadOnlyModelViewSet): # 情報を参照するだけなのでReadOnly
    # Infomationモデルの一覧GET,詳細GETを行うAPI
    queryset = Infomation.objects.all() # modelにDB操作のqueryを送る(filterかけて一部を取り出すとかできる)
    serializer_class = InfomationSerializer # serializeするクラスを指定

    # Infomation.objects.order_by(“-created_at”)[0:100] # 作成日順に先頭100件
    
