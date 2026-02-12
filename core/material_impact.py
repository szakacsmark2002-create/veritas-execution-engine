from typing import Dict, List, Optional
from core.model import Entity, MaterialStatus, StateStatus
from core.sla import evaluate_sla


def calculate_material_impact(
    material_id: str,
    all_entities: List[Entity]
) -> Dict[str, object]:
    """
    Calculează impactul unui material asupra tuturor orderelor.
    Caută material_id în entity.materials pentru toate entitățile.
    """

    impacted_orders = []
    blocked_orders = []
    at_risk_orders = []
    delayed_orders = []
    ok_orders = []

    sla_breached = 0
    sla_at_risk = 0

    # agregări cantitative (minim, V1)
    total_required = 0
    total_available = 0

    # meta despre material (dacă îl găsim undeva)
    observed_statuses = {}
    inbound_etas = []

    for e in all_entities:
        if not e.materials:
            continue

        matched = None
        for m in e.materials:
            if m.id == material_id:
                matched = m
                break

        if not matched:
            continue

        impacted_orders.append(e.id)

        # totals
        total_required += int(matched.required_qty)
        total_available += int(matched.available_qty)

        # status stats
        observed_statuses[matched.status.value] = observed_statuses.get(matched.status.value, 0) + 1
        if matched.status == MaterialStatus.INBOUND and matched.eta:
            inbound_etas.append(matched.eta)

        # bucket by state
        st = e.state.status
        if st == StateStatus.BLOCKED:
            blocked_orders.append(e.id)
        elif st == StateStatus.AT_RISK:
            at_risk_orders.append(e.id)
        elif st == StateStatus.DELAYED:
            delayed_orders.append(e.id)
        else:
            ok_orders.append(e.id)

        # SLA buckets
        sla = evaluate_sla(e)
        if sla.get("sla_status") == "breached":
            sla_breached += 1
        elif sla.get("sla_status") == "at_risk":
            sla_at_risk += 1

    severity = "low"
    if sla_breached > 0 or len(blocked_orders) > 0:
        severity = "high"
    elif sla_at_risk > 0 or len(at_risk_orders) > 0:
        severity = "medium"

    next_inbound_eta: Optional[str] = None
    if inbound_etas:
        next_inbound_eta = min(inbound_etas).isoformat()

    return {
        "material_id": material_id,
        "impacted_orders_count": len(impacted_orders),
        "impacted_orders": impacted_orders,
        "by_state": {
            "blocked": blocked_orders,
            "at_risk": at_risk_orders,
            "delayed": delayed_orders,
            "ok": ok_orders,
        },
        "sla": {
            "breached": sla_breached,
            "at_risk": sla_at_risk,
        },
        "quantities": {
            "total_required": total_required,
            "total_available": total_available,
            "shortage": max(0, total_required - total_available),
        },
        "observed_material_statuses": observed_statuses,
        "next_inbound_eta": next_inbound_eta,
        "severity": severity,
    }

