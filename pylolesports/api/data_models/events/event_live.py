from dataclasses import dataclass
from typing import List

@dataclass
class EventLiveTeamResult:
    gameWins: int
    outcome: str

@dataclass
class EventLiveTeamRecord:
    losses: str
    wins: str

@dataclass
class EventLiveStrategy:
    count:int
    type: str

@dataclass
class EventLiveMatchTeam:
    code: str
    image: str
    name: str
    result: EventLiveTeamResult
    slug: str
    record: EventLiveTeamRecord

@dataclass
class EventLiveMatch:
    teams: List[EventLiveMatchTeam]
    id: str
    strategy: EventLiveStrategy


@dataclass
class EventLiveEventTournament:
    id: str

@dataclass
class EventLiveLeague:
    name: str
    slug: str
    id: str
    image: str
    priority: int

@dataclass
class EventLiveEvent:
    startTime: str
    state: str
    type: str
    id: str
    league: EventLiveLeague
    tournament: EventLiveEventTournament
    streams: None
    blockName: str = None
    match: EventLiveMatch = None

@dataclass
class LiveSchedule:
    events: List[EventLiveEvent]
