from setuptools import setup, find_packages
from flask_captcha2.auther import __version__, __NAME__, __short_description__, __author__, __author_mail__

with open("./README.md", "r") as f:
    long_description = f.read()


setup(
    name=__NAME__ ,
    version=__version__,
    description=__short_description__,
    packages=find_packages(),
    author_email=__author_mail__,
    author=__author__,
    url="https://github.com/alisharify7/flask_captcha2",
    long_description=long_description,
    # long_description_content_type="text/x-rst",
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    license="MIT",
    install_requires=[
        "flask>=2.2.5",
        "markupsafe>=2.1.2",
        "requests>=2.30.0"
    ],
    python_requires=">=3.8",
    keywords='flask security, Google captcha for flask, captcha , flask, flask-captcha, flask-captcha2, flask_captcha2'

)
