from setuptools import setup, find_packages

__NAME__ = "Flask-captcha2"
__version__ = "3.0.5"
__author__ = "ali sharify"
__author_mail__ = "alisharifyofficial@gmail.com"
__copyright__ = "ali sharify - 2023"
__license__ = "MIT"
__short_description__ = "Flask plugin to integrate Google captcha (version 2, 3) and local captcha (image, voice) with Flask applications"


with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name=__NAME__,
    version=__version__,
    description=__short_description__,
    packages=find_packages(),
    author_email=__author_mail__,
    author=__author__,
    url="https://github.com/alisharify7/flask_captcha2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Environment :: Web Environment",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Framework :: Flask",
    ],
    license="MIT",
    install_requires=[
        "flask>=2.2.5",
        "markupsafe>=2.1.2",
        "requests>=2.30.0",
        "captcha>=0.5.0"
    ],
    python_requires=">=3.8",
    keywords='flask security, Google captcha for flask, captcha , flask, flask-captcha, flask-captcha2, flask_captcha2, flask-images-captcha'

)
