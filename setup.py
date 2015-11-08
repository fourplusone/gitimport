from setuptools import setup, Extension

setup(
    name='gitimport',
    description='',
    author_email='mba@fourplusone.de',

    packages=['gitimport'],
    version='1.0.0',
    requires=['pygit2'],
)