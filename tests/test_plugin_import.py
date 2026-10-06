def test_asset_server_plugin_is_importable():
    from plugins.asset_server import AssetServerClient, AssetPolicy

    assert AssetServerClient is not None
    assert AssetPolicy is not None
