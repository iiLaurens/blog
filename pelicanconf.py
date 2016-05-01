#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'Laurens'
SITENAME = u'Laurens\' geeky adventures'
SITEURL = 'http://blog.laurens.xyz'

TIMEZONE = 'Europe/Paris'

DEFAULT_DATE_FORMAT = '%d-%m-%Y'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
FEED_ALL_RSS = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

# Blogroll
LINKS = None

HIDE_SIDEBAR = True

BANNER = False

DISPLAY_PAGES_ON_MENU = True
DISPLAY_CATEGORIES_ON_MENU = False

DEFAULT_PAGINATION = 5

TAG_CLOUD_MAX_ITEMS = 10

DISPLAY_TAGS_ON_SIDEBAR = False

THEME = "themes/Bootstrap3"

PYGMENTS_STYLE = "zenburn"

BOOTSTRAP_THEME = 'yeti'

PLUGIN_PATHS = ['plugins']

DIRECT_TEMPLATES = ('index', 'archives', 'search', 'tags')

DISPLAY_ARTICLE_INFO_ON_INDEX = True

PLUGINS = ['tipue_search']

DISQUS_SITENAME = 'iilaurens'
#ADDTHIS_PROFILE = 'ra-520d4af6518bf3c7'

STATIC_PATHS = ['images', 'files', 'extra/CNAME']
EXTRA_PATH_METADATA = {'extra/CNAME': {'path': 'CNAME'},}

ARTICLE_URL = 'post/{slug}.html'
ARTICLE_SAVE_AS = 'post/{slug}.html'
PAGE_URL = '{slug}.html'
PAGE_SAVE_AS = '{slug}.html'
TAG_URL = 'tags/{slug}.html'
TAG_SAVE_AS = 'tags/{slug}.html'
TAGS_URL = 'tags.html'

GOOGLE_ANALYTICS = "UA-77190701-1"
