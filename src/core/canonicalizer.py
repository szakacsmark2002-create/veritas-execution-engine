import json
import unicodedata
from decimal import Decimal


def normalize_string(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def normalize_value(value):
    if isinstance(value, str):
        return normalize_string(value)

    if isinstance(value, float):
        raise ValueError("Float values are not allowed. Use Decimal or string.")

    if isinstance(value, Decimal):
        return format(value, "f")

    if isinstance(value, dict):
        return {
            key: normalize_value(value[key])
            for key in sorted(value.keys())
        }

    if isinstance(value, list):
        return [normalize_value(item) for item in value]

    return value


def canonicalize(data) -> str:
    normalized = normalize_value(data)
    return json.dumps(
        normalized,
        ensure_ascii=False,
        separators=(",", ":"),
    )
