from dataclasses import dataclass


@dataclass
class Pokemon:
    id: int
    name: str
    type: str
    height: float
    weight: float

@dataclass
class Owner:
    id: int
    name: str
    town: str
