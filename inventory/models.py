from django.db import models
from django.utils import timezone

class InventoryItem(models.Model):
    name = models.CharField("食品名", max_length=100)
    expiration_date = models.DateField("賞味期限")

    def __str__(self) -> str:
        return self.name
    
    @property
    def days_left(self) -> int:
        """
        賞味期限までの残り日数（今日基準）。
        expiration_date は必須フィールドの前提。
        """
        return (self.expiration_date - timezone.localdate()).days