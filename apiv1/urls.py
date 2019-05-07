from django.urls import path, include
from rest_framework import routers
from . import views # apiv1のviewsをimport
# or from .views import InfomationViewSet

# routerにViewSetを登録することで、URLのパターン作成を自動でやってくれる
router = routers.DefaultRouter()
router.register("infomation", views.InfomationViewSet) # InfomationViewSetをrouterに設定する

# routerをincludeして、URL判定をrouterに任せる
urlpatterns = [
    path('', include(router.urls)),
]

# TODO routerもうちょいしっかり理解