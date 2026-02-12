import hashlib


def sha256_hash(data: str) -> str:
    if not isinstance(data, str):
        raise TypeError("Data must be a string before hashing.")

    return hashlib.sha256(data.encode("utf-8")).hexdigest()
