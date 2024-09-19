

def test_settings():
    from publisher.settings import app_settings

    assert len(str(app_settings.API_TOKEN)) > 0
