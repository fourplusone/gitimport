from setuptools import setup, Extension

setup(
    name='gitimport',
    description='Import python packages directly from a git repository',
    author='Matthias Bartelmeß',
    author_email='mba@fourplusone.de',
    py_modules=['gitimport'],
    version='1.0.0',
    install_requires=['pygit2'],
)