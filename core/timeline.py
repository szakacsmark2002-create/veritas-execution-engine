from datetime import datetime
from typing import Dict
from core.sla import evaluate_sla
from core.model import Entity


def build_timeline(entity: Entity) -> Dict[str, object]:
    """
    Construiește un timeline complet pentru o entitate.
B    """
    timeline = {
        "id": entity.id,
        "type": entity.type,
        "state": {
            "status": entity.state.status,
            "reason": entity.state.reason
        }
    }

    if entity.time:
        timeline["time"] = {
            "start": entity.time.start,
            "eta": entity.time.eta,
            "now": datetime.now()
        }

    timeline["sla"] = evaluate_sla(entity)

    if entity.constraint:
        timeline["constraint"] = {
            "type": entity.constraint.type
        }
 
    if entity.materials:
        timeline["materials"] = [
            {
                "id": m.id,
                "status": m.status.value,
                "required_qty": m.required_qty,
                "available_qty": m.available_qty,
                "eta": m.eta
            }
            for m in entity.materials
        ]

    return timeline

