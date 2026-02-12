from typing import List
from core.model import Entity, StateStatus


PRIORITY_ORDER = {
    StateStatus.BLOCKED: 1,
    StateStatus.DELAYED: 2,
    StateStatus.AT_RISK: 3,
    StateStatus.PARTIAL: 4,
    StateStatus.OK: 5,
}


def list_problematic_entities(entities: List[Entity]) -> List[Entity]:
    """
    Returnează entitățile ordonate după severitatea problemei.
    """
    return sorted(
        entities,
        key=lambda e: PRIORITY_ORDER.get(e.state.status, 99)
    )

