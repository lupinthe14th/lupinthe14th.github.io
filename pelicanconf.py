#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Hideo Suzuki'
SITENAME = u'engineering note'
SITEURL = 'http://lupinthe14th.github.io'

PATH = 'content'

TIMEZONE = 'Asia/Tokyo'

DEFAULT_LANG = 'ja'

DATE_FORMATS = {
    'en': '%a, %d %b %Y',
    'jp': '%Y-%m-%d(%a)',
}

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('running & climbing', 'http://running-climbing.tumblr.com', ),)

# Social widget
SOCIAL = (('twitter', 'https://twitter.com/hideosuzuki2'),
          ('facebook', 'https://www.facebook.com/hideo.suzukithe13th'),
          ('github', 'http://github.com/lupinthe14th'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

# Pygments
PYGMENTS_STYLE = 'zenburn'

# GitHub Flavored Markdown
MARKDOWN = {    
    'extension_configs': {
        'mdx_linkify': {},
    #    'mdx_del_ins': {},
    #    'markdown_checklist.extension': {},
        'markdown.extensions.sane_lists': {},
        'markdown.extensions.fenced_code': {},
        'markdown.extensions.codehilite': {'css_class': 'highlight'},
        'markdown.extensions.tables': {},
        'markdown.extensions.extra': {},
        'markdown.extensions.toc': {},
        'markdown.extensions.footnotes' : {},
        'markdown.extensions.meta': {},
    },
    'output_format': 'html5',
}
# Pelican Plugins setting
PLUGIN_PATHS = ['./pelican-plugins']
PLUGINS = [
    # 'assets',
    'sitemap',
    'gravatar',
    'tag_cloud',
    'tipue_search',
    'i18n_subsites',
]
I18N_TEMPLATES_LANG = 'ja'

# sitemap
SITEMAP = {'format': 'xml', 'priorities': {'articles': 0.5, 'indexes': 0.5,
                                           'pages': 0.5}, 'changefreqs': {
    'articles': 'monthly',
    'indexes': 'daily', 'pages':
    'monthly'}}

# Theme
THEME = './pelican-themes/pelican-bootstrap3'

# pelican-bootstrap3 setting
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
DISPLAY_TAGS_ON_SIDEBAR = True
DISPLAY_TAGS_INLINE = True
DISPLAY_CATEGORIES_ON_SIDEBAR = True
DISPLAY_RECENT_POSTS_ON_SIDEBAR = True
RECENT_POST_COUNT = True

# AddThis
ADDTHIS_PROFILE = 'ra-564f240ac6e6866c'

# Facebook Open Graph
USE_OPEN_GRAPH = True
OPEN_GRAPH_FB_APP_ID = '925856150831958'

# Twitter Cards
TWITTER_CARDS = True

# Twitter Timeline
# TWITTER_USERNAME = 'hideosuzuki2'
# TWITTER_WIDGET_ID = '667706264785281024'

# Amazon affiliate
AMAZON_AD_TAG = 'lupinthe14t05-22'

# Google AdSense
# GOOGLE_AD_CLIENT = '-pub-5121601573225140'
# GOOGLE_AD_SLOT = ''
# GOOGLE_AD_CLIENT_1 = ''
GOOGLE_AD_CLIENT_1 = 'a-pub-5121601573225140'
# GOOGLE_AD_SLOT_1 = ''

# Content license
CC_LICENSE = 'CC-BY'

# Gravatar
AUTHOR_EMAIL = 'hideosuzuki@fb4.so-net.ne.jp'

# Tipue Search
DIRECT_TEMPLATES = ('index', 'categories', 'authors', 'archives', 'search')
# SEARCH_URL = 'http://lupinthe14th.github.io'

# Site Brand
# SITELOGO = 'images/logo.png'

# Custom CSS
CUSTOM_CSS = 'static/custom.css'

# Tell Pelican to add 'extra/custom.css' to the output dir
STATIC_PATHS = ['images', 'extra/custom.css']

# Tell Pelican to change the path to 'static/custom.css' in the output dir
EXTRA_PATH_METADATA = {
    'extra/custom.css': {'path': 'static/custom.css'}
}
