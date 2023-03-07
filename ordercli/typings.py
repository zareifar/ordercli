from typing import List, TypedDict


class NourishDish(TypedDict):
    id: int
    name: str


class NourishMenu(TypedDict):
    dishes: List[NourishDish]
