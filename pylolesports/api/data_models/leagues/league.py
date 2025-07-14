from dataclasses import dataclass

@dataclass
class League:
    name: str
    slug: str
    id: str
    image: str
    priority: int
    region: str
    displayPriority: dict = None
