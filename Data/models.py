from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Point:
    longitude: float
    latitude: float

@dataclass
class Sighting:
    id: int = field(default=0)
    title: str = field(default="")
    sighting_date: datetime = field(default=datetime.now())
    description: str = field(default="")
    coords: Point = field(default=Point(0.0, 0.0))
    duration: str = field(default="")
    user_id: int = field(default=0)
    creation_date: datetime = field(default=datetime.now())

# TODO: add other types
