from fastapi import FastAPI

from src.core.canonicalizer import canonicalize
from src.core.hasher import sha256_hash
from src.core.engine import execution_pipeline
from src.storage.db import (
    insert_execution,
    get_previous_execution_hash,
    get_execution_by_id,
    get_previous_by_sequence,
    get_all_executions_ordered
)

app = FastAPI(
    title="SACO – Integrity Engine",
    description="Deterministic Operational Integrity Engine. Decisions You Can Defend.",
    version="1.0.0"
)



@app.get("/health")
def health():
    return {"status": "SACO_IS_OK"}

@app.get("/about")
def about():
    return {
        "product": "SACO – Integrity Engine",
        "tagline": "Decisions You Can Defend.",
        "core_principles": [
            "Deterministic execution",
            "Cryptographic verification",
            "Replayable decision context",
            "Tamper-evident ledger"
        ]
    }


@app.get("/test-hash")
def test_hash():
    sample_input = {
        "b": 2,
        "a": 1
    }

    canonical = canonicalize(sample_input)
    hashed = sha256_hash(canonical)

    return {
        "canonical": canonical,
        "hash": hashed
    }


@app.get("/execute-test")
def execute_test():

    input_data = {"x": 10, "y": 5}
    world_snapshot = {"orders": [1, 2, 3], "materials": ["A", "B"]}

    previous_hash = get_previous_execution_hash()

    record = execution_pipeline(input_data, world_snapshot, previous_hash)

    execution_id = insert_execution(record, previous_hash)

    record["execution_id"] = execution_id

    return record


@app.get("/verify-chain")
def verify_chain():

    rows = get_all_executions_ordered()

    if not rows:
        return {"ok": True, "message": "ledger empty"}

    previous_hash = None

    for row in rows:

        # 1. Verify link
        if row["previous_execution_hash"] != previous_hash:
            return {
                "ok": False,
                "error": "link broken",
                "sequence_number": row["sequence_number"],
                "expected_previous_hash": previous_hash,
                "stored_previous_hash": row["previous_execution_hash"]
            }

        # 2. Recompute input/world/result hashes
        input_canonical = canonicalize(row["input_json"])
        world_canonical = canonicalize(row["world_json"])
        result_canonical = canonicalize(row["result_json"])

        input_hash = sha256_hash(input_canonical)
        world_hash = sha256_hash(world_canonical)
        result_hash = sha256_hash(result_canonical)

        if (
            input_hash != row["input_hash"] or
            world_hash != row["world_hash"] or
            result_hash != row["result_hash"]
        ):
            return {
                "ok": False,
                "error": "data tampered",
                "sequence_number": row["sequence_number"]
            }

        # 3. Recompute execution hash
        fingerprint = canonicalize({
            "previous_execution_hash": previous_hash,
            "input_hash": input_hash,
            "world_hash": world_hash,
            "result_hash": result_hash,
            "engine_version": row["engine_version"],
            "schema_version": row["schema_version"],
        })

        execution_hash = sha256_hash(fingerprint)

        if execution_hash != row["execution_hash"]:
            return {
                "ok": False,
                "error": "execution hash mismatch",
                "sequence_number": row["sequence_number"]
            }

        previous_hash = execution_hash

    return {
        "ok": True,
        "verified_blocks": len(rows)
    }
