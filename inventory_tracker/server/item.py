import dataclasses
from typing import Optional


@dataclasses.dataclass
class Item:
    """Item aka material, unique type of inventory."""

    id: Optional[int]
    name: str
    description: str

    def as_dict(self):
        return dataclasses.asdict(self)
