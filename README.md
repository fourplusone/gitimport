# gitimport
Import python packages directly from a git repository

[![Build Status](https://travis-ci.org/fourplusone/gitimport.svg?branch=master)](https://travis-ci.org/fourplusone/gitimport)


## System Requirements

- Python 3.4 or higher
- libgit2 installed

## Installation

### Mac OS X

`brew install libgit2`

### All Platforms

`pip3 install gitimport`

## Usage 

### A simple example

```python
import gitimport

path = gitimport.repository_path('/path/to/your/repo', repo, rev="demo")

# Now you can import 'your_module' from the git repository
import your_module
```
