from core.model import Entity, ConstraintType


def explain_entity(entity: Entity) -> dict:
    """
    Generează o explicație structurată pentru o entitate.
    """
    explanation = {
        "id": entity.id,
        "type": entity.type,
        "status": entity.state.status,
        "summary": "",
        "details": [],
        "impact": "",
        "recommendation": ""
    }

    if entity.constraint:
        ct = entity.constraint.type

        if ct == ConstraintType.MATERIAL_MISSING:
            explanation["summary"] = "Entity is blocked due to missing material."
            explanation["details"].append("Required material is not available in stock.")
            explanation["impact"] = "Process cannot continue until material is available."
            explanation["recommendation"] = "Check inbound or substitute material."

        elif ct == ConstraintType.TIME_DELAY:
            explanation["summary"] = "Entity is delayed due to time constraints."
            explanation["details"].append("Expected completion time has been exceeded.")
            explanation["impact"] = "Potential SLA breach."
            explanation["recommendation"] = "Replan timeline or prioritize this entity."

        else:
            explanation["summary"] = "Entity is at risk due to an operational constraint."
            explanation["details"].append("A non-specific constraint was detected.")
            explanation["impact"] = "May affect downstream processes."
            explanation["recommendation"] = "Investigate constraint details."

    else:
        explanation["summary"] = "Entity is in a healthy state."
        explanation["impact"] = "No immediate action required."
        explanation["recommendation"] = "Continue monitoring."

    return explanation

