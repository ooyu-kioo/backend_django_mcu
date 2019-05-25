from django.urls import path, include
from rest_framework import routers
from . import views  # apiv1のviewsをimport
# or from .views import InfomationViewSet

# routerにViewSetを登録することで、URLのパターン作成を自動でやってくれる
router = routers.DefaultRouter()

# InfomationViewSet, ReleaseInfoViewSetをrouterに設定する(URLに対応するview関数のセット)
router.register("infomation", views.InfomationViewSet)
router.register("releaseInfo", views.ReleaseInfoViewSet)

# routerをincludeして、URL判定をrouterに任せる
urlpatterns = [
    path('', include(router.urls)),
]

# TODO routerもうちょいしっかり理解
