def interpret_question(text: str) -> dict:
    text = text.lower()

    if "sla" in text:
        if "risc" in text or "risk" in text:
            return {"intent": "sla_at_risk"}
        if "ratat" in text or "breach" in text:
            return {"intent": "sla_breached"}
        return {"intent": "sla_overview"}

    if "daca" in text and ("intarzie" in text or "delay" in text):
        hours = 48
        for token in text.split():
            if token.isdigit():
                hours = int(token)
                break
        return {"intent": "simulate_delay", "delay_hours": hours}

    if "probleme" in text or "blocat" in text:
        return {"intent": "list_problematic", "scope": "orders"}

    if "de ce" in text and "order" in text:
        return {"intent": "explain_entity", "entity_type": "order"}

    return {"intent": "unknown"}

