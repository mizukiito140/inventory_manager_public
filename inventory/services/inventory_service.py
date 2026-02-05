from django.db.models import QuerySet
from ..models import InventoryItem


def get_items() -> QuerySet[InventoryItem]:
    """
    在庫アイテムを新しい順で取得する。
    days_left は InventoryItem.days_left @property で計算される。
    """
    return InventoryItem.objects.all().order_by("-id")