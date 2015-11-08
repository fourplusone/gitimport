from setuptools import setup, Extension

setup(
    name='gitimport',
    description='Import python packages directly from a git repository',
    author_email='mba@fourplusone.de',
    py_modules=['gitimport'],
    version='1.0.0',
    requires=['pygit2'],
)