from setuptools import setup, find_packages
from flask_captcha2.auther import __version__

with open("./readme.md") as f:
    long_description = f.read()

setup(
    name="flask_captcha2",
    version=__version__,
    description="an light and simple flask extension for integrate google recaptcha with Flask Apps",
    packages=find_packages(),
    author_email="alisharifyofficial@gmail.com",
    author="Ali Sharify",
    url="https://github.com/alisharify7/flask_captcha2",
    long_description=long_description,
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
    python_requires=">=3.8"
)
