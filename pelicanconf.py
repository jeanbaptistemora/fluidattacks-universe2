#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Site information
AUTHOR = 'FLUID'
SITENAME = 'A Pentesting Company | FLUID'
SITEURL = 'http://localhost:8000/web/en'

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
TAGS_SAVE_AS = 'tags/index.html'
TAGS_URL = 'tags/'
TAG_SAVE_AS = 'tags/{slug}/index.html'
TAG_URL = 'tags/{slug}/'
AUTHORS_SAVE_AS = 'authors/index.html'
AUTHORS_URL = 'authors/'
AUTHOR_SAVE_AS = 'authors/{slug}/index.html'
AUTHOR_URL = 'authors/{slug}/'
CATEGORIES_SAVE_AS = 'categories/index.html'
CATEGORIES_URL = 'categories/'
CATEGORY_SAVE_AS = 'categories/{slug}/index.html'
CATEGORY_URL = 'categories/{slug}/'
USE_FOLDER_AS_CATEGORY = False
INDEX_SAVE_AS = 'blog/index.html'
LANDING_SAVE_AS = 'index.html'
ERROR_SAVE_AS = 'error/index.html'

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
           'tag_cloud'
]
RELATED_POSTS_MAX = 3
DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'archives', 'authors', 'search', 'landing', 'error'))
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
        'SITEURL': 'http://localhost:8000/web/es',
        'OUTPUT_PATH': 'output/web/es',
        'THEME': 'theme/2014',
        'ARTICLE_PATHS': ['blog-es'],
        'PAGE_PATHS': ['pages-es', 'kb'],
        'PAGE_SAVE_AS': 'pages-es/{slug}index.html',
        'ARTICLE_SAVE_AS': 'blog-es/{slug}index.html',
        'STATIC_PATHS': ['files', 'images', 'blog-es', 'kb', 'pages-es'],
        'GOOGLE_ANALYTICS': 'UA-22974464-4',
        'TAGS_SAVE_AS': 'etiquetas/index.html',
        'TAGS_URL': 'etiquetas/',
        'TAG_SAVE_AS': 'etiquetas/{slug}/index.html',
        'TAG_URL': 'etiquetas/{slug}/',
        'AUTHORS_SAVE_AS': 'autores/index.html',
        'AUTHORS_URL': 'autores/',
        'AUTHOR_SAVE_AS': 'autores/{slug}/index.html',
        'AUTHOR_URL': 'autores/{slug}/',
        'CATEGORIES_SAVE_AS': 'categorias/index.html',
        'CATEGORIES_URL': 'categorias/',
        'CATEGORY_SAVE_AS': 'categorias/{slug}/index.html',
        'CATEGORY_URL': 'categorias/{slug}/',
        'ASCIIDOC_OPTIONS': ['-f /etc/asciidoc/lang-es.conf'],
    }
}
lang_siteurls = {
     'en': 'http://localhost:8000/web/en',
     'es': 'http://localhost:8000/web/es',
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
