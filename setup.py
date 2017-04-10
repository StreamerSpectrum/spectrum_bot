''' Setup dependancies for SpectrumBot '''

from setuptools import setup, find_packages

setup(
    name="SpectrumBot",
    version="0.1.0",
    url="https://github.com/StreamerSpectrum/spectrum_bot",
    author="CAPGames (@CAPGamesUK)",
    author_email="",
    description="All in 1 Chat and Interactive bot for Beam.",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests_oauthlib"]
)
