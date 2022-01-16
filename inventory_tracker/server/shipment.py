import dataclasses
from typing import Optional


@dataclasses.dataclass
class Shipment:
    """Shipment information."""

    id: Optional[int]
    address: str

    def as_dict(self):
        return dataclasses.asdict(self)


@dataclasses.dataclass
class ShipmentInventoryItem:
    """Items and quantities in a shipment."""

    id: Optional[int]
    shipment_id: int
    item_id: int
    quantity: int

    def as_dict(self):
        return dataclasses.asdict(self)
