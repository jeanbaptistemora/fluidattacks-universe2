#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Site information
AUTHOR = 'FLUID'
SITENAME = 'FLUID | Pentesting, Ethical Hacking, Análisis de Código'
SITEURL = 'https://fluid.la/site'
PATH = 'content'

# Date and time configuration
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

# Articles per page
DEFAULT_PAGINATION = 12

# URLs format
ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'
PAGE_PATHS = ['pages']

# Images and files path
STATIC_PATHS = ['images', 'files']

# Plugins configuration
PLUGIN_PATHS = 'pelican-plugins'
PLUGINS = [
           'asciidoc_reader',
           'assets',
           'neighbors',
           'share_post',
           'related_posts',
           'representative_image',
           'tipue_search',
           'sitemap'
]
RELATED_POSTS_MAX = 3
DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'archives', 'authors', 'search', '404'))
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.7,
        'indexes': 0.8,
        'pages': 0.9
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

# Disqus
DISQUS_SITENAME = 'fluid-blog'

# Theme
THEME = 'theme/pelican-clean-blog'

# Google Analytics
GOOGLE_ANALYTICS = 'UA-22974464-4'
