from asset_platform.domain.services import content_hash, extract_spatial_metadata


def test_content_hash_is_deterministic():
    assert content_hash("abc") == content_hash("abc")
    assert content_hash("abc") != content_hash("abcd")


def test_spatial_metadata():
    result = extract_spatial_metadata("mesh.glb", "abc", "GLB")
    assert result["format"] == "glb"
    assert result["coordinate_system"] == "local-space"
