from typing import List, Dict
from core.model import Entity, StateStatus, ConstraintType


def calculate_time_impact(entities: List[Entity]) -> Dict[str, int]:
    impact = {
        "blocked": 0,
        "delayed": 0,
        "at_risk": 0,
        "ok": 0
    }

    for e in entities:
        if e.state.status == StateStatus.BLOCKED:
            impact["blocked"] += 1
        elif e.state.status == StateStatus.DELAYED:
            impact["delayed"] += 1
        elif e.state.status == StateStatus.AT_RISK:
            impact["at_risk"] += 1
        else:
            impact["ok"] += 1

    return impact


def simulate_inbound_delay(
    entities: List[Entity],
    delay_hours: int
) -> Dict[str, object]:
    affected = []

    for e in entities:
        if e.constraint and e.constraint.type == ConstraintType.DEPENDENCY:
            affected.append(e.id)

    return {
        "simulated_delay_hours": delay_hours,
        "affected_orders": affected,
        "affected_count": len(affected)
    }

