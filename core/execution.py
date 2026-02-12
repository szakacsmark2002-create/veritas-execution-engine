from datetime import datetime
from core.hashing import deterministic_hash

CORE_VERSION = "0.2.0"


class ExecutionContext:
    def __init__(self, question: str, world_snapshot):
        self.timestamp = datetime.utcnow().isoformat()
        self.core_version = CORE_VERSION
        self.question = question

        self.input_hash = deterministic_hash(question)
        self.world_hash = world_snapshot.dataset_hash

        self.execution_id = deterministic_hash({
            "timestamp": self.timestamp,
            "input_hash": self.input_hash,
            "world_hash": self.world_hash
        })

        self.result_hash = None

    def attach_result(self, result: dict):
        self.result_hash = deterministic_hash(result)

