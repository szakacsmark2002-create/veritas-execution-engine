from typing import Dict, Optional
from core.model import EntityType


# =========================
# SEMANTIC VOCABULARY
# =========================

SEMANTIC_MAP = {
    "OPSOPS_FLAG_X9": {
        "entity_type": EntityType.LOCATION,
        "semantic": "warehouse_zone",
        "aliases": [
            "lagerzone",
            "zona_depozit",
            "raktár_zóna",
            "wh_area"
        ]
    },

    "OPSLAG0_STZ99": {
        "entity_type": EntityType.LOCATION,
        "semantic": "storage_zone",
        "aliases": [
            "opslag_zone",
            "storage_area",
            "stoc_zona",
            "raktár_tér"
        ]
    }
}


def resolve_field(
    erp_field: str,
    value: Optional[str] = None
) -> Optional[Dict[str, str]]:
    """
    Rezolvă semantic un câmp ERP dacă există mapping.
    """
    mapping = SEMANTIC_MAP.get(erp_field)

    if not mapping:
        return None

    return {
        "entity_type": mapping["entity_type"],
        "semantic": mapping["semantic"],
        "value": value
    }

