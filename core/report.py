from typing import Dict, List
from core.model import Entity
from core.timeline import build_timeline
from core.impact import calculate_operational_impact


def build_order_report(
    target: Entity,
    all_entities: List[Entity]
) -> Dict[str, object]:
    """
    Construiește raportul complet pentru un order.
    """

    timeline = build_timeline(target)
    impact = calculate_operational_impact(target, all_entities)

    # rezumat executiv (management-ready)
    executive_summary = {
        "order_id": target.id,
        "status": timeline["state"]["status"].value,
        "sla_status": timeline["sla"]["sla_status"],
        "severity": impact["severity"],
        "affected_orders": impact["affected_orders_count"],
        "root_cause": impact["root_cause"]
    }

    return {
        "executive_summary": executive_summary,
        "timeline": timeline,
        "impact": impact
    }

