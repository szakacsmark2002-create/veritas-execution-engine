from src.core.canonicalizer import canonicalize
from src.core.hasher import sha256_hash

ENGINE_VERSION = "2.0.0"
SCHEMA_VERSION = "1.0.0"


def execute(input_data: dict, world_snapshot: dict) -> dict:
    # Dummy deterministic logic
    return {
        "input_sum": sum(input_data.values()),
        "world_size": len(world_snapshot),
    }


def execution_pipeline(input_data: dict, world_snapshot: dict, previous_execution_hash: str | None) -> dict:
    canonical_input = canonicalize(input_data)
    input_hash = sha256_hash(canonical_input)

    canonical_world = canonicalize(world_snapshot)
    world_hash = sha256_hash(canonical_world)

    result = execute(input_data, world_snapshot)

    canonical_result = canonicalize(result)
    result_hash = sha256_hash(canonical_result)

    # IMPORTANT: previous_execution_hash is part of the fingerprint
    execution_fingerprint = canonicalize({
        "previous_execution_hash": previous_execution_hash,
        "input_hash": input_hash,
        "world_hash": world_hash,
        "result_hash": result_hash,
        "engine_version": ENGINE_VERSION,
        "schema_version": SCHEMA_VERSION,
    })

    execution_hash = sha256_hash(execution_fingerprint)

    return {
        "engine_version": ENGINE_VERSION,
        "schema_version": SCHEMA_VERSION,
        "previous_execution_hash": previous_execution_hash,
        "input_hash": input_hash,
        "world_hash": world_hash,
        "result_hash": result_hash,
        "execution_hash": execution_hash,
        "input": input_data,
        "world": world_snapshot,
        "result": result,
    }
