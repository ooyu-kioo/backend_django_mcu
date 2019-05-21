#
# DBのmodel設定：
#

import uuid
from django.db import models
from django.utils import timezone

# Create your models here.


class Infomation(models.Model):  # django標準のmodelクラスを継承

    class Meta:
        db_table = "infomation"

    # カラム名定義
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)  # ユニバーサルな一意のid
    artist_name = models.CharField(max_length=300)
    info_title = models.CharField(max_length=300)
    info_body_link = models.CharField(
        max_length=300, unique=True)  # info詳細のリンク
    created_at = models.DateTimeField(default=timezone.now)  # 作成日時

    # 管理ページ表示用
    def __str__(self):
        return self.artist_name

# CharField：文字列
# IntegerField：数値
# DateField：日付

# null：True,False
# blank、dafault、unique、verbose_name
