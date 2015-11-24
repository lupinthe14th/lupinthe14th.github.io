#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'http://lupinthe14th.github.io'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "engineeringnote"
DISQUS_NO_ID = True
DISQUS_ID_PREFIX_SLUG = True
DISQUS_DISPLAY_COUNTS = True

GOOGLE_ANALYTICS_UNIVERSAL = "UA-70443206-1"
GOOGLE_ANALYTICS_UNIVERSAL_PROPERTY = "auto"
