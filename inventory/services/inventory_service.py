from datetime import date
from typing import List

from ..models import InventoryItem


def get_items_with_days_left() -> List[InventoryItem]:
    items = list(InventoryItem.objects.all().order_by("-id"))
    today = date.today()

    for item in items:
        if item.expiration_date:
            item.days_left = (item.expiration_date - today).days
        else:
            item.days_left = None
    return items
