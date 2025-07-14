from dataclasses import dataclass, field
from typing import List

@dataclass
class LeagueStandingsTeamResult:
    gameWins: int
    outcome: str = None

@dataclass
class LeagueStandingsTeamRecord:
    losses: str
    wins: str

@dataclass
class LeagueStandingsMatchTeam:
    code: str
    image: str
    name: str
    id: str
    slug: str
    result: LeagueStandingsTeamResult | None

@dataclass
class LeagueStandingsRankingTeam:
    code: str
    image: str
    name: str
    id: str
    slug: str
    record: LeagueStandingsTeamRecord = None

@dataclass
class LeagueStandingsMatch:
    teams: List[LeagueStandingsMatchTeam]
    id: str
    state: str
    previousMatchIds: List[str]
    flags: str

@dataclass
class LeagueStandingsRanking:
    ordinal: int
    team: List[LeagueStandingsRankingTeam] | None

@dataclass
class LeagueStandingsSection:
    name: str
    matches: List[LeagueStandingsMatch]
    rankings: list[LeagueStandingsRanking]

@dataclass
class LeagueStandingsStage:
    name: str
    type: None
    slug: str
    sections: List[LeagueStandingsSection]

@dataclass
class LeagueStandingsInnerModels:
    # created to make importing the models easier
    team_result     : LeagueStandingsTeamResult
    team_record     : LeagueStandingsTeamRecord
    match_team      : LeagueStandingsMatchTeam
    ranking_team    : LeagueStandingsRankingTeam
    match           : LeagueStandingsMatch
    ranking         : LeagueStandingsRanking
    section         : LeagueStandingsSection
    stage           : LeagueStandingsStage

@dataclass
class Standing:
    stages: List[LeagueStandingsStage]
