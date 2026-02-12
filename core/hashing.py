import hashlib
import json


def deterministic_hash(data: object) -> str:
    """
    Stable SHA256 hash for structured data.
    """
    serialized = json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        default=str
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

