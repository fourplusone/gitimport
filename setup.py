from setuptools import setup, Extension

setup(
    name='gitimport',
    description='Import python packages directly from a git repository',
    long_description='',
    author='Matthias Bartelmeß',
    author_email='mba@fourplusone.de',
    url='https://github.com/fourplusone/gitimport',
    py_modules=['gitimport'],
    version='1.1.0',
    install_requires=['pygit2'],
    license='MIT',
    classifiers=['Development Status :: 4 - Beta', 
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3 :: Only']
)