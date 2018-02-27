#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Site information
AUTHOR = 'FLUID'
SITENAME = 'A Pentesting Company | FLUID'
SITEURL = '/web/en'

# Theme
THEME = 'theme/2018'

# Date and time configuration
TIMEZONE = 'America/Bogota'
DEFAULT_DATE_FORMAT = ('%Y-%m-%d')
DEFAULT_LANG = 'en'
OUTPUT_PATH = 'public/en'

# URLs format
PATH = 'content'
ARTICLE_PATHS = ['blog-en']
PAGE_PATHS = ['pages-en-2018']
STATIC_PATHS = ['images', 'files', 'blog-en', 'pages-en-2018']
ARTICLE_URL = 'blog/{slug}'
ARTICLE_SAVE_AS = 'blog-en/{slug}index.html'
DRAFT_URL = 'drafts/{slug}'
DRAFT_SAVE_AS = 'drafts/{slug}index.html'
PAGE_URL = '{slug}'
PAGE_SAVE_AS = 'pages-en-2018/{slug}index.html'
TAGS_SAVE_AS = 'blog/tags/index.html'
TAGS_URL = 'blog/tags/'
TAG_SAVE_AS = 'blog/tags/{slug}/index.html'
TAG_URL = 'blog/tags/{slug}/'
AUTHORS_SAVE_AS = 'blog/authors/index.html'
AUTHORS_URL = 'blog/authors/'
AUTHOR_SAVE_AS = 'blog/authors/{slug}/index.html'
AUTHOR_URL = 'blog/authors/{slug}/'
CATEGORIES_SAVE_AS = 'blog/categories/index.html'
CATEGORIES_URL = 'blog/categories/'
CATEGORY_SAVE_AS = 'blog/categories/{slug}/index.html'
CATEGORY_URL = 'blog/categories/{slug}/'
USE_FOLDER_AS_CATEGORY = False

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
DIRECT_TEMPLATES = (('index', 'tags', 'categories', 'archives', 'authors', 'search'))
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
        'SITEURL': '/web/es',
        'OUTPUT_PATH': 'public/es',
        'THEME': 'theme/2018',
        'ARTICLE_PATHS': ['blog-es'],
        'PAGE_PATHS': ['pages-es-2018', 'defends'],
        'PAGE_SAVE_AS': 'pages-es-2018/{slug}index.html',
        'ARTICLE_SAVE_AS': 'blog-es/{slug}index.html',
        'STATIC_PATHS': ['files', 'images', 'blog-es', 'defends', 'pages-es-2018'],
        'GOOGLE_ANALYTICS': 'UA-22974464-4',
        'TAGS_SAVE_AS': 'blog/etiquetas/index.html',
        'TAGS_URL': 'blog/etiquetas/',
        'TAG_SAVE_AS': 'blog/etiquetas/{slug}/index.html',
        'TAG_URL': 'blog/etiquetas/{slug}/',
        'AUTHORS_SAVE_AS': 'blog/autores/index.html',
        'AUTHORS_URL': 'blog/autores/',
        'AUTHOR_SAVE_AS': 'blog/autores/{slug}/index.html',
        'AUTHOR_URL': 'blog/autores/{slug}/',
        'CATEGORIES_SAVE_AS': 'blog/categorias/index.html',
        'CATEGORIES_URL': 'blog/categorias/',
        'CATEGORY_SAVE_AS': 'blog/categorias/{slug}/index.html',
        'CATEGORY_URL': 'blog/categorias/{slug}/',
        'ASCIIDOC_OPTIONS': ['-f /etc/asciidoc/lang-es.conf'],
    }
}
lang_siteurls = {
     'en': '/web/en',
     'es': '/web/es',
}
REDIRECT_SAVE_AS = PAGE_SAVE_AS
ASSET_BUNDLES = (
  ('bundle', [
   'css/custom/general.scss',
   'css/custom/global.scss',
   'css/custom/custom.scss'
  ], {'filters': 'scss'}),
)

# Cache Settings
CHECK_MODIFIED_METHOD = 'md5'
CACHE_CONTENT = True
LOAD_CONTENT_CACHE = True

# Disqus
DISQUS_SITENAME = 'fluidsignal'

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
