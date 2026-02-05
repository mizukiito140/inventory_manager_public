from typing import List

from ..models import InventoryItem


def get_items() -> List[InventoryItem]:
    """
    在庫アイテムを新しい順で取得する。
    days_left は InventoryItem.days_left @property で計算される。
    """
    return list(InventoryItem.objects.all().order_by("-id"))