#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Site information
AUTHOR = 'FLUID'
SITENAME = 'A Pentesting Company | FLUID'
SITEURL = 'https://fluid.la/web/en'

# Theme
THEME = 'theme/2014'

# Date and time configuration
TIMEZONE = 'America/Bogota'
DEFAULT_DATE_FORMAT = ('%Y-%m-%d')
DEFAULT_LANG = 'en'
OUTPUT_PATH = 'output/web/en'

# URLs format
PATH = 'content'
ARTICLE_PATHS = ['blog-en']
PAGE_PATHS = ['pages-en']
STATIC_PATHS = ['images', 'files', 'blog-en', 'pages-en']
ARTICLE_URL = 'blog/{slug}'
ARTICLE_SAVE_AS = 'blog-en/{slug}index.html'
PAGE_URL = '{slug}'
PAGE_SAVE_AS = 'pages-en/{slug}index.html'
KB_SAVE_AS = 'kb/index.html'

# Plugins configuration
PLUGIN_PATHS = ['/app/pelican-plugins']
PLUGINS = [
           'asciidoc_reader',
           'assets',
           'neighbors',
           'share_post',
           'related_posts',
           'representative_image',
           'tipue_search',
           'sitemap',
           'i18n_subsites',
           'pelican-redirect',
]
RELATED_POSTS_MAX = 3
DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'archives', 'authors', 'search', '404', 'kb'))
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
# Line that allows the localization of the site (traslation)
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n']}
I18N_SUBSITES = {
    'es': {
        'SITENAME': 'Especialistas en Ethical Hacking | FLUID',
        'SITEURL': 'https://fluid.la/web/es',
        'OUTPUT_PATH': 'output/web/es',
        'THEME': 'theme/2014',
        'ARTICLE_PATHS': ['blog-es'],
        'PAGE_PATHS': ['pages-es', 'kb'],
        'PAGE_SAVE_AS': 'pages-es/{slug}index.html',
        'ARTICLE_SAVE_AS': 'blog-es/{slug}index.html',
        'STATIC_PATHS': ['files', 'images', 'blog-es', 'kb', 'pages-es'],
        'GOOGLE_ANALYTICS': 'UA-22974464-4',
        }
}
lang_siteurls = {
     'en': 'https://fluid.la/web/en',
     'es': 'https://fluid.la/web/es',
}
REDIRECT_SAVE_AS = PAGE_SAVE_AS
ASSET_BUNDLES = (
  ('bundle', [
   'css/custom/general.scss',
   'css/custom/global.scss',
   'css/custom/custom.scss'
  ], {'filters': 'scss'}),
)

# Disqus
DISQUS_SITENAME = 'fluidsignal'

# Google Analytics
GOOGLE_ANALYTICS = 'UA-22974464-11'

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
