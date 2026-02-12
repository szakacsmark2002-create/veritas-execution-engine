from datetime import datetime
from core.hashing import deterministic_hash


def _serialize_entity(e):
    if hasattr(e, "__dict__"):
        return {
            k: v
            for k, v in sorted(e.__dict__.items())
            if not k.startswith("_")
        }
    return e


class WorldSnapshot:
    def __init__(self, entities: list, source: str = "mock"):
        self.created_at = datetime.utcnow().isoformat()
        self.source = source
        self.entity_count = len(entities)

        serialized_entities = [
            _serialize_entity(e)
            for e in entities
        ]

        self.dataset_hash = deterministic_hash(serialized_entities)

        self.snapshot_id = deterministic_hash({
            "dataset_hash": self.dataset_hash
        })

