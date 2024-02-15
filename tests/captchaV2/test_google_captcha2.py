import pytest
from markupsafe import Markup


def test_captcha_config_is_correct(googlecaptcha2, app):
    """This test ensure that Flask-Captcha can read and apply all config correctly
    from app.config object to google-captcha-v2 object"""
    assert googlecaptcha2.PRIVATE_KEY == app.config.get("CAPTCHA_PRIVATE_KEY")
    assert googlecaptcha2.PUBLIC_KEY == app.config.get("CAPTCHA_PUBLIC_KEY")
    assert googlecaptcha2.ENABLED == app.config.get("CAPTCHA_ENABLED")
    assert googlecaptcha2.CAPTCHA_LOG == app.config.get("CAPTCHA_LOG")
    assert googlecaptcha2.LANGUAGE == app.config.get("CAPTCHA_LANGUAGE")
    assert googlecaptcha2.TABINDEX == app.config.get("CAPTCHA_TABINDEX")
    assert googlecaptcha2.SIZE == app.config.get("CAPTCHA_SIZE")
    assert googlecaptcha2.TYPE == app.config.get("CAPTCHA_TYPE")
    assert googlecaptcha2.THEME == app.config.get("CAPTCHA_THEME")


def test_refresh_captcha_config(googlecaptcha2, app):
    """Test refresh method work properly"""
    # change the app config while the app running <captcha config in app.config>
    app.config["CAPTCHA_LOG"] = True
    assert googlecaptcha2.CAPTCHA_LOG != app.config["CAPTCHA_LOG"]

    googlecaptcha2.refresh_conf(app)  # refresh new config from flask App
    assert googlecaptcha2.CAPTCHA_LOG == app.config["CAPTCHA_LOG"]


def test_load_captcha_in_html(client, googlecaptcha2, app):
    with pytest.raises(ValueError) as e:
        captcha = app.template_context_processors[None][-1]()['captcha'].render_captcha(model_name='unknown-name')

    captcha = app.template_context_processors[None][-1]()['captcha'].render_captcha(model_name='flask-captcha-v2')
    assert isinstance(captcha, Markup)
    assert f"data-sitekey=\"{googlecaptcha2.PUBLIC_KEY}\"" in captcha
    assert f"data-type=\"{googlecaptcha2.TYPE}\"" in captcha
    assert f"data-lang=\"{googlecaptcha2.LANGUAGE}\"" in captcha
    assert f"data-size=\"{googlecaptcha2.SIZE}\"" in captcha
    assert f"data-size=\"{googlecaptcha2.SIZE}\"" in captcha
    assert f"data-tabindex=\"{googlecaptcha2.TABINDEX}\"" in captcha


def test_captcha_enable_on(app, googlecaptcha2, client):
    """if enable is false render_captcha always return " " and
      is_verify method always return True
    """

    googlecaptcha2.ENABLED = False
    captcha = app.template_context_processors[None][-1]()['captcha'].render_captcha(model_name='flask-captcha-v2')
    assert captcha == Markup(' ')

    @app.post("/test-invalid-post/")
    def post_invalid():
        if googlecaptcha2.is_verify():
            return "OK"
        return "NOT OK"

    response = client.post("/test-invalid-post/")
    assert b'OK' == response.get_data()


def test_captcha_enable_off(app, googlecaptcha2, client):
    """if enable is True render_captcha returns a valid captcha and
      is_verify method checks the response with google
    """

    captcha = app.template_context_processors[None][-1]()['captcha'].render_captcha(model_name='flask-captcha-v2')
    assert captcha != Markup(' ')  # captcha is on so its should render captcha widget in html

    @app.post("/test-invalid-post/")
    def post_invalid():
        if googlecaptcha2.is_verify():
            return "OK"
        return "NOT OK"

    response = client.post("/test-invalid-post/", data={'g-CAPTCHA-response': 'invalid string'})
    assert b'NOT OK' == response.get_data()
