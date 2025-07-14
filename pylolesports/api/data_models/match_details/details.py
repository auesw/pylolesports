from dataclasses import dataclass
from typing import List

@dataclass
class PerkMetadata:
    styleId: int
    subStyleId: int
    perks: List[int]

@dataclass
class ParticipantStatsExtended:
    participantId: int
    level: int
    kills: int
    deaths: int
    assists: int
    creepScore: int
    totalGoldEarned: int
    killParticipation: float
    championDamageShare: float
    wardsPlaced: int
    wardsDestroyed: int
    attackDamage: int
    abilityPower: int
    criticalChance: float
    attackSpeed: int
    lifeSteal: int
    armor: int
    magicResistance: int
    tenacity: float
    items: List[int]
    perkMetadata: PerkMetadata
    abilities: List[str]
    totalGold: int = None
    currentHealth: int = None
    maxHealth: int = None

@dataclass
class Frame:
    rfc460Timestamp: str
    participants: List[ParticipantStatsExtended]