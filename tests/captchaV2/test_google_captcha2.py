def test_captcha_config_is_correct(googlecaptcha2, app):
    """This test ensure that Flask-Captcha can read and apply all config correctly
    from app.config object to google-captcha-v2 object"""
    assert googlecaptcha2.PRIVATE_KEY == app.config.get("RECAPTCHA_PRIVATE_KEY")
    assert googlecaptcha2.PUBLIC_KEY == app.config.get("RECAPTCHA_PUBLIC_KEY")
    assert googlecaptcha2.ENABLED == app.config.get("RECAPTCHA_ENABLED")
    assert googlecaptcha2.CAPTCHA_LOG == app.config.get("RECAPTCHA_LOG")
    assert googlecaptcha2.LANGUAGE == app.config.get("RECAPTCHA_LANGUAGE")
    assert googlecaptcha2.TABINDEX == app.config.get("RECAPTCHA_TABINDEX")
    assert googlecaptcha2.SIZE == app.config.get("RECAPTCHA_SIZE")
    assert googlecaptcha2.TYPE == app.config.get("RECAPTCHA_TYPE")
    assert googlecaptcha2.THEME == app.config.get("RECAPTCHA_THEME")


def test_refresh_captcha_config(googlecaptcha2, app):
    """Test refresh method work properly"""
    # change the app config while the app running <captcha config in app.config>
    app.config["RECAPTCHA_LOG"] = False
    assert googlecaptcha2.CAPTCHA_LOG != app.config["RECAPTCHA_LOG"]

    googlecaptcha2.refresh_conf(app)  # refresh new config from flask App
    assert googlecaptcha2.CAPTCHA_LOG == app.config["RECAPTCHA_LOG"]


def test_load_captcha_in_html():
    ...


def test_captcha_valid_key():
    ...


def test_captcha_invalid_key():
    ...
