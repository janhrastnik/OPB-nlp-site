from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from datetime import datetime

@dataclass_json
@dataclass
class Sighting:
    id: int = field(default=0)
    title: str = field(default="")
    sighting_date: datetime = field(default=datetime.now())
    description: str = field(default="")
    coords: str = field(default="")
    duration: str = field(default="")
    user_id: int = field(default=0)
    creation_date: datetime = field(default=datetime.now())

@dataclass_json
@dataclass
class User:
    id: int = field(default=0)
    username: str = field(default="")
    email: str = field(default="")
    password: str = field(default="")
# TODO: add other types
