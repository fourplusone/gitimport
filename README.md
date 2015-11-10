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
import sys
import gitimport
import pygit2

# Add gitimport to pythons import machinary
gitimport.add_gitimporter_path_hook()

repo = pygit2.Repository('/path/to/your/repo')

# Create a path for the current 'demo' branch.
path = gitimport.repository_path(repo, rev="demo")

# Insert this path into sys.path
sys.path.insert(0, path)

# Now you can import 'your_module' from the git repository
import your_module
```
