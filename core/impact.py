from typing import Dict, List
from core.model import Entity, StateStatus
from core.sla import evaluate_sla


def calculate_operational_impact(
    target: Entity,
    all_entities: List[Entity]
) -> Dict[str, object]:
    """
    Calculează impactul operațional al unei entități asupra sistemului.
    """
    affected_orders = []
    sla_at_risk = 0
    sla_breached = 0
    root_causes = {}

    for e in all_entities:
        if e.id == target.id:
            continue

        # dependență simplă: dacă target e blocat, alții pot fi afectați
        if target.state.status == StateStatus.BLOCKED:
            affected_orders.append(e.id)

            sla = evaluate_sla(e)
            if sla.get("sla_status") == "at_risk":
                sla_at_risk += 1
            if sla.get("sla_status") == "breached":
                sla_breached += 1

    # root cause
    if target.constraint:
        cause = target.constraint.type.value
        root_causes[cause] = root_causes.get(cause, 0) + 1

    # severitate simplă (V1)
    severity = "low"
    if sla_breached > 0:
        severity = "high"
    elif sla_at_risk > 0:
        severity = "medium"

    return {
        "affected_orders_count": len(affected_orders),
        "affected_orders": affected_orders,
        "sla_at_risk": sla_at_risk,
        "sla_breached": sla_breached,
        "root_cause": max(root_causes, key=root_causes.get) if root_causes else None,
        "severity": severity
    }

