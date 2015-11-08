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

```python
import sys
import gitimport
gitimport.add_gitimporter_path_hook()

sys.path.insert(0, '/path/to/your/repo@2af8daa')

import your_module

```
