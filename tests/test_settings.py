

def test_settings():
    from publisher.settings import app_settings, prices_settings

    assert len(str(app_settings.API_TOKEN)) > 0
    assert len(prices_settings.keys()) > 0
