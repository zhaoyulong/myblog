#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://zhaoyulong.github.io/'
RELATIVE_URLS = False

DELETE_OUTPUT_DIRECTORY = True
OUTPUT_PATH = '../zhaoyulong.github.io/'
OUTPUT_RETENTION = ['.git','README.md']

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
