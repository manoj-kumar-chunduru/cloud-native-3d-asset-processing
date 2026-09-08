from asset_platform.domain.models import Asset
from asset_platform.domain.services import extract_spatial_metadata

def process_asset(asset: Asset) -> dict:
    return {
        "asset_id": asset.asset_id,
        "validation": {"valid": True, "format": asset.format.lower()},
        "spatial": extract_spatial_metadata(asset.name, "x" * asset.size_bytes, asset.format),
        "processing_version": "1.0",
    }
