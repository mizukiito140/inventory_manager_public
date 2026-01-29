from django.db import models

class InventoryItem(models.Model):
    name = models.CharField("食品名", max_length=100)
    expiration_date = models.DateField("賞味期限")

    def __str__(self):
        return self.name