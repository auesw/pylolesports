from dataclasses import dataclass
from typing import List

@dataclass
class ParticipantMetadata:
    participantId: int
    summonerName: str
    championId: str
    role: str

@dataclass
class ParticipantMetadataExtended(ParticipantMetadata):
    esportsPlayerId: str

@dataclass
class TeamMetadata:
    esportsTeamId: str
    participantMetadata: List[ParticipantMetadata] | List[ParticipantMetadataExtended]

@dataclass
class GameMetadata:
    patchVersion: str
    blueTeamMetadata: TeamMetadata
    redTeamMetadata: TeamMetadata

@dataclass
class ParticipantStats:
    participantId: int
    level: int
    kills: int
    deaths: int
    assists: int
    creepScore: int
    totalGold: int
    currentHealth: int
    maxHealth: int

@dataclass
class TeamStats:
    totalGold: int
    inhibitors: int
    towers: int
    barons: int
    totalKills: int
    dragons: int
    participants: ParticipantStats

@dataclass
class WindowFrame:
    rfc460Timestamp: str
    gameState: str
    blueTeam: TeamStats
    redTeam: TeamStats

@dataclass
class Window:
    esportsGameId: str
    esportsMatchId: str
    gameMetadata: GameMetadata
    frames: List[WindowFrame]