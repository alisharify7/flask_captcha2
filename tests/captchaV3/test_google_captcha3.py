import pytest
from markupsafe import Markup


def test_captcha_config_is_correct(googlecaptcha3, app):
    """This test ensure that Flask-Captcha can read and apply all config correctly
    from app.config object to google-captcha-v2 object"""
    assert googlecaptcha3.PRIVATE_KEY == app.config.get("CAPTCHA_PRIVATE_KEY")
    assert googlecaptcha3.PUBLIC_KEY == app.config.get("CAPTCHA_PUBLIC_KEY")
    assert googlecaptcha3.ENABLED == app.config.get("CAPTCHA_ENABLED")
    assert googlecaptcha3.CAPTCHA_LOG == app.config.get("CAPTCHA_LOG")
    assert googlecaptcha3.SCORE == app.config.get("CAPTCHA_SCORE")
    assert googlecaptcha3.MINIMUM_SCORE == 0.5


def test_refresh_captcha_config(googlecaptcha3, app):
    """Test refresh method work properly"""
    # change the app config while the app running <captcha config in app.config>
    app.config["CAPTCHA_LOG"] = True
    assert googlecaptcha3.CAPTCHA_LOG != app.config["CAPTCHA_LOG"]

    googlecaptcha3.refresh_conf(app)  # refresh new config from flask App
    assert googlecaptcha3.CAPTCHA_LOG == app.config["CAPTCHA_LOG"]


def test_load_captcha_in_html(client, googlecaptcha3, app, captcha3_template_conf):
    with pytest.raises(Exception) as e:
        # test unknown name
        captcha = app.template_context_processors[None][-1]()['captcha'].render_captcha(model_name='unknown-name')

    captcha = app.template_context_processors[None][-1]()['captcha'].render_captcha(model_name='flask-captcha-v3',
                                                                                    **captcha3_template_conf)
    assert isinstance(captcha, Markup)
    assert f"data-sitekey=\"{googlecaptcha3.PUBLIC_KEY}\"" in captcha
    assert f"class=\"g-recaptcha {captcha3_template_conf['class']}\"" in captcha
    assert f"{captcha3_template_conf['dataset']}" in captcha
    assert f"id=\"{captcha3_template_conf['id']}\"" in captcha
    assert f"{captcha3_template_conf['button_text']}" in captcha

    # check captcha badge in the eight bottom os the screen in hidden or not
    captcha3_template_conf['hide_badge'] = True
    captcha = app.template_context_processors[None][-1]()['captcha'].render_captcha(model_name='flask-captcha-v3',
                                                                                    **captcha3_template_conf)
    hidden_badge_style = Markup("<style>.grecaptcha-badge {visibility: hidden;}</style>")
    assert hidden_badge_style in captcha


def test_captcha_enable_on(app, googlecaptcha3, client, captcha3_template_conf):
    """if enable is set to false render_captcha always return an empty string " " and
      is_verify method always return True
    """

    googlecaptcha3.ENABLED = False
    captcha = app.template_context_processors[None][-1]()['captcha'].render_captcha(model_name='flask-captcha-v3',
                                                                                    conf=captcha3_template_conf)
    assert captcha != Markup(" ")  # return default input-type submit

    @app.post("/test-invalid-post/")
    def post_invalid():
        if googlecaptcha3.is_verify():
            return "OK"
        return "NOT OK"

    response = client.post("/test-invalid-post/")
    assert b'OK' == response.get_data()


def test_captcha_enable_off(app, googlecaptcha3, client, captcha3_template_conf):
    """if enable is True render_captcha returns a valid captcha and
      is_verify method checks the response with google
    """

    captcha = app.template_context_processors[None][-1]()['captcha'].render_captcha(model_name='flask-captcha-v3',
                                                                                    conf=captcha3_template_conf)
    assert captcha != Markup(' ')  # captcha is on so its should render captcha widget in html

    @app.post("/test-invalid-post/")
    def post_invalid():
        if googlecaptcha3.is_verify():
            return "OK"
        return "NOT OK"

    response = client.post("/test-invalid-post/", data={'g-CAPTCHA-response': 'invalid string'})
    assert b'NOT OK' == response.get_data()
