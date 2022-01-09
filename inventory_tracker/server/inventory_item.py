import dataclasses
from typing import Optional

@dataclasses.dataclass
class InventoryItem:
    """Item with quantity."""
    id: Optional[int]
    item_id: int
    quantity: int

    def as_dict(self):
        return dataclasses.asdict(self)