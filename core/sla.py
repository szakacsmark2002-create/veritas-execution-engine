from datetime import datetime
from typing import Dict
from core.model import Entity, StateStatus


def evaluate_sla(entity: Entity) -> Dict[str, object]:
    """
    Evaluează riscul de SLA pentru o entitate.
    """
    if not entity.time or not entity.time.eta:
        return {
            "sla_status": "unknown",
            "reason": "no ETA defined"
        }

    now = datetime.now()
    eta = entity.time.eta

    if now > eta:
        return {
            "sla_status": "breached",
            "minutes_overdue": int((now - eta).total_seconds() / 60)
        }

    minutes_left = int((eta - now).total_seconds() / 60)

    if minutes_left < 60:
        return {
            "sla_status": "at_risk",
            "minutes_left": minutes_left
        }

    return {
        "sla_status": "on_track",
        "minutes_left": minutes_left
    }

