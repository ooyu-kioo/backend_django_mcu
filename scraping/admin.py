#
# 管理画面の設定：
#

from django.contrib import admin
from .models import Infomation

# 管理画面に表示するapp登録
class InfomationModelAdmin(admin.ModelAdmin):
    list_display = ("id", "artist_name", "info_title", "info_body_link", "created_at") # 表示項目
    ordering = ("-created_at",) # sort

    # readonly_fields = ("id") ：管理画面からいじられたくない項目

admin.site.register(Infomation, InfomationModelAdmin)
