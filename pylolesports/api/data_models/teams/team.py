from dataclasses import dataclass
from typing import List

@dataclass
class HomeLeague:
    name: str
    region: str

@dataclass
class Player:
    id: str
    summonerName: str
    firstName: str
    lastName: str
    image: str
    role: str

@dataclass
class Team:
    code: str
    image: str
    name: str
    id: str
    slug: str
    alternativeImage: str
    homeLeague: HomeLeague
    backgroundImage: None
    status: None
    players: List[Player]
