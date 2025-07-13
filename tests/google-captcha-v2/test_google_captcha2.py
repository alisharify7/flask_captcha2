import pytest
from markupsafe import Markup

@pytest.mark.config_g2_simple
def test_captcha_config_is_correct(googlecaptcha2_simple, app):
    """This test ensure that Flask-Captcha can read and apply all config correctly
    from app.config object to google-captcha-v2 object"""
    assert googlecaptcha2_simple.PRIVATE_KEY == app.config.get("captcha_private_key")
    assert googlecaptcha2_simple.PUBLIC_KEY == app.config.get("captcha_public_key")
    assert googlecaptcha2_simple.ENABLED == app.config.get("captcha_enabled")
    assert googlecaptcha2_simple.CAPTCHA_LOG == app.config.get("captcha_log")
    assert googlecaptcha2_simple.LANGUAGE == app.config.get("captcha_language")
    assert googlecaptcha2_simple.TABINDEX == app.config.get("captcha_tabindex")
    assert googlecaptcha2_simple.SIZE == app.config.get("captcha_size")
    assert googlecaptcha2_simple.TYPE == app.config.get("captcha_type")
    assert googlecaptcha2_simple.THEME == app.config.get("captcha_theme")



@pytest.mark.config_g2_hidden
def test_captcha_hidden_config_is_correct(googlecaptcha2_hidden, app):
    """Ensure that Flask-Captcha configures Google Captcha v2 with 'invisible' mode correctly"""
    assert googlecaptcha2_hidden.PRIVATE_KEY == app.config.get("captcha_private_key")
    assert googlecaptcha2_hidden.PUBLIC_KEY == app.config.get("captcha_public_key")
    assert googlecaptcha2_hidden.ENABLED == app.config.get("captcha_enabled")
    assert googlecaptcha2_hidden.CAPTCHA_LOG == app.config.get("captcha_log")
    assert googlecaptcha2_hidden.LANGUAGE == app.config.get("captcha_language")
    assert googlecaptcha2_hidden.TABINDEX == app.config.get("captcha_tabindex")
    assert googlecaptcha2_hidden.SIZE == app.config.get("captcha_size")
    assert googlecaptcha2_hidden.TYPE == app.config.get("captcha_type")
    assert googlecaptcha2_hidden.THEME == app.config.get("captcha_theme")


@pytest.mark.config_g3
def test_captcha_v3_config_is_correct(googlecaptcha3, app):
    """Ensure that Flask-Captcha correctly reads and applies config for Google Captcha v3"""
    assert googlecaptcha3.PRIVATE_KEY == app.config.get("captcha_private_key")
    assert googlecaptcha3.PUBLIC_KEY == app.config.get("captcha_public_key")
    assert googlecaptcha3.ENABLED == app.config.get("captcha_enabled")
    assert googlecaptcha3.SCORE == app.config.get("captcha_score")
    assert googlecaptcha3.CAPTCHA_LOG == app.config.get("captcha_log")

    
def test_refresh_captcha_config(googlecaptcha2, app):
    """Test refresh method work properly"""
    # change the app config while the app running <captcha config in app.config>
    app.config["CAPTCHA_LOG"] = True
    assert googlecaptcha2.CAPTCHA_LOG != app.config["CAPTCHA_LOG"]

    googlecaptcha2.refresh_conf(app)  # refresh new config from flask App
    assert googlecaptcha2.CAPTCHA_LOG == app.config["CAPTCHA_LOG"]


def test_load_captcha_in_html(client, googlecaptcha2, app):
    with pytest.raises(Exception) as e:
        captcha = app.template_context_processors[None][-1]()[
            "captcha"
        ].render_captcha(model_name="unknown-name")

    captcha = app.template_context_processors[None][-1]()[
        "captcha"
    ].render_captcha(model_name="flask-captcha-v2")
    assert isinstance(captcha, Markup)
    assert f'data-sitekey="{googlecaptcha2.PUBLIC_KEY}"' in captcha
    assert f'data-type="{googlecaptcha2.TYPE}"' in captcha
    assert f'data-lang="{googlecaptcha2.LANGUAGE}"' in captcha
    assert f'data-size="{googlecaptcha2.SIZE}"' in captcha
    assert f'data-size="{googlecaptcha2.SIZE}"' in captcha
    assert f'data-tabindex="{googlecaptcha2.TABINDEX}"' in captcha


def test_captcha_enable_on(app, googlecaptcha2, client):
    """if enable is false render_captcha always return " " and
    is_verify method always return True
    """

    googlecaptcha2.ENABLED = False
    captcha = app.template_context_processors[None][-1]()[
        "captcha"
    ].render_captcha(model_name="flask-captcha-v2")
    assert captcha == Markup(" ")

    @app.post("/test-invalid-post/")
    def post_invalid():
        if googlecaptcha2.is_verify():
            return "OK"
        return "NOT OK"

    response = client.post("/test-invalid-post/")
    assert b"OK" == response.get_data()


def test_captcha_enable_off(app, googlecaptcha2, client):
    """if enable is True render_captcha returns a valid captcha and
    is_verify method checks the response with google
    """

    captcha = app.template_context_processors[None][-1]()[
        "captcha"
    ].render_captcha(model_name="flask-captcha-v2")
    assert captcha != Markup(
        " "
    )  # captcha is on so its should render captcha widget in html

    @app.post("/test-invalid-post/")
    def post_invalid():
        if googlecaptcha2.is_verify():
            return "OK"
        return "NOT OK"

    response = client.post(
        "/test-invalid-post/", data={"g-CAPTCHA-response": "invalid string"}
    )
    assert b"NOT OK" == response.get_data()
