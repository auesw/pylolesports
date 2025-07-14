from dataclasses import dataclass, field
from typing import List

@dataclass
class EventSchedulePages:
    older: str
    newer: str

@dataclass
class EventScheduleTeamResult:
    gameWins: int
    outcome: str

@dataclass
class EventScheduleTeamRecord:
    losses: str
    wins: str

@dataclass
class EventScheduleMatchTeam:
    code: str
    image: str
    name: str
    result: EventScheduleTeamResult
    record: EventScheduleTeamRecord

@dataclass
class EventScheduleStrategy:
    count: int
    type: str = None

@dataclass
class EventScheduleMatch:
    teams: List[EventScheduleMatchTeam]
    id: str
    strategy: EventScheduleStrategy
    flags: list = None

@dataclass
class EventScheduleLeague:
    name: str
    slug: str

@dataclass
class EventScheduleEvent:
    startTime: str
    blockName: str
    match: EventScheduleMatch
    state: str
    type: str
    league: EventScheduleLeague

@dataclass
class Schedule:
    pages: EventSchedulePages
    events: List[EventScheduleEvent]
    updated: str = None
