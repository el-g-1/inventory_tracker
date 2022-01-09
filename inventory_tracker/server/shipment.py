from dataclasses import dataclass
from typing import List

@dataclass
class Shipment:
    """Items and quantities in a shipment."""
    id: int
    address: str
    inventory_item_ids: List[int]