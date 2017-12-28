#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Site information
AUTHOR = 'FLUID'
SITENAME = 'FLUID | Pentesting, Ethical Hacking, Code Analysis'
SITEURL = 'https://fluid.la/web/en'

# Theme
THEME = 'theme/pelican-clean-blog'

# Date and time configuration
TIMEZONE = 'America/Bogota'
DEFAULT_DATE_FORMAT = ('%Y-%m-%d')
DEFAULT_LANG = 'en'
OUTPUT_PATH = 'output/web/en'

# URLs format
PATH = 'content'
ARTICLE_PATHS = ['blog-en']
PAGE_PATHS = ['pages-en']
STATIC_PATHS = ['images', 'files', 'blog-en']
ARTICLE_URL = 'blog/{slug}/'
ARTICLE_SAVE_AS = 'blog-en/{slug}/index.html'
PAGE_URL = '{slug}/'
PAGE_SAVE_AS = '{slug}/index.html'

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
           'sitemap',
           'i18n_subsites'
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
DEFAULT_PAGINATION = 12
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
I18N_SUBSITES = {
    'es': {
        'SITENAME': 'FLUID | Pentesting, Ethical Hacking, Análisis de Código',
        'SITEURL': 'https://fluid.la/web/es',
        'OUTPUT_PATH': 'output/web/es',
        'THEME': 'theme/pelican-clean-blog',
        'ARTICLE_PATHS': ['blog-es'],
        'PAGE_PATHS': ['pages-es'],
        'ARTICLE_SAVE_AS': 'blog-es/{slug}/index.html',
        'STATIC_PATHS': ['files', 'images', 'blog-es']
        }
}
lang_siteurls = {
     'en': 'https://fluid.la/web/en',
     'es': 'https://fluid.la/web/es',
}

# Disqus
DISQUS_SITENAME = 'fluidsignal'

# Google Analytics
GOOGLE_ANALYTICS = 'UA-22974464-4'

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
