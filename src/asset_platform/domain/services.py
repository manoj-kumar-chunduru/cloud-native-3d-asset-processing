import hashlib


def content_hash(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def extract_spatial_metadata(name: str, content: str, asset_format: str) -> dict:
    # Lightweight deterministic metadata extraction suitable for a reference service.
    return {
        "format": asset_format.lower(),
        "content_length": len(content.encode("utf-8")),
        "name_length": len(name),
        "coordinate_system": "local-space",
        "bounds": {"min": [0, 0, 0], "max": [1, 1, 1]},
    }
