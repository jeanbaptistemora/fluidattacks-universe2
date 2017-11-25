#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

AUTHOR = 'FLUID'
SITENAME = 'Blog de FLUID'
SITEURL = 'http://blog2.fluid.la'

PATH = 'content'

TIMEZONE = 'America/Bogota'

DEFAULT_DATE_FORMAT = ('%Y-%m-%d')

DEFAULT_LANG = 'Spanish'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 9

# Formating URLs
#ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
#ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'
PAGE_PATHS = ['pages']

#Images
STATIC_PATHS = ['images']

# Plugins
PLUGIN_PATHS = 'pelican-plugins'
PLUGINS = ['asciidoc_reader','assets','neighbors','share_post','related_posts','representative_image']

RELATED_POSTS_MAX = 3

# Discus
DISQUS_SITENAME = 'fluid-blog'


# theme
THEME = "theme/pelican-clean-blog"


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
