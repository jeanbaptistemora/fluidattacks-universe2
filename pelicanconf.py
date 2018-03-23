#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

# Site information
AUTHOR = 'FLUIDAttacks'

# Theme
THEME = 'theme/2014'

# Date and time configuration
TIMEZONE = 'America/Bogota'
DEFAULT_DATE_FORMAT = ('%Y-%m-%d')
DEFAULT_LANG = 'de'
OUTPUT_PATH = 'output/web/de'

# URLs format
PATH = 'content'
ARTICLE_PATHS = ['blog']
PAGE_PATHS = ['pages']
ARTICLE_URL = 'blog/{slug}'
ARTICLE_SAVE_AS = 'blog/{slug}index.html'
PAGE_URL = '{slug}'
PAGE_SAVE_AS = 'pages/{slug}index.html'
DRAFT_URL = 'drafts/{slug}'
DRAFT_SAVE_AS = 'drafts/{slug}index.html'
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
    'en': {
        'SITENAME': 'A Pentesting Company | FLUIDAttacks',
        'SITEURL': 'https://fluidattacks.com/web/en',
        'SUBSITEURL': 'https://fluidattacks.com/web/es',
        'OUTPUT_PATH': 'output/web/en',
        'THEME': 'theme/2014',
        'ARTICLE_PATHS': ['blog-en'],
        'PAGE_PATHS': ['pages-en'],
        'PAGE_SAVE_AS': 'pages-en/{slug}index.html',
        'ARTICLE_SAVE_AS': 'blog-en/{slug}index.html',
        'STATIC_PATHS': ['files', 'images', 'blog-en', 'pages-en'],
        'TAGS_SAVE_AS': 'blog/tags/index.html',
        'TAGS_URL': 'blog/tags/',
        'TAG_SAVE_AS': 'blog/tags/{slug}/index.html',
        'TAG_URL': 'blog/tags/{slug}/',
        'AUTHORS_SAVE_AS': 'blog/authors/index.html',
        'AUTHORS_URL': 'blog/authors/',
        'AUTHOR_SAVE_AS': 'blog/authors/{slug}/index.html',
        'AUTHOR_URL': 'blog/authors/{slug}/',
        'CATEGORIES_SAVE_AS': 'blog/categories/index.html',
        'CATEGORIES_URL': 'blog/categories/',
        'CATEGORY_SAVE_AS': 'blog/categories/{slug}/index.html',
        'CATEGORY_URL': 'blog/categories/{slug}/',
        'ASCIIDOC_OPTIONS': ['-a icons', '-a iconsdir=/web/en/images/icons',
                             '-a tooltip=/web/en/images/icons/tooltip.png'],
    },
    'es': {
        'SITENAME': 'Especialistas en Ethical Hacking | FLUIDAttacks',
        'SITEURL': 'https://fluidattacks.com/web/es',
        'SUBSITEURL': 'https://fluidattacks.com/web/en',
        'OUTPUT_PATH': 'output/web/es',
        'THEME': 'theme/2014',
        'ARTICLE_PATHS': ['blog-es'],
        'PAGE_PATHS': ['pages-es', 'defends'],
        'PAGE_SAVE_AS': 'pages-es/{slug}index.html',
        'ARTICLE_SAVE_AS': 'blog-es/{slug}index.html',
        'STATIC_PATHS': ['files', 'images', 'blog-es', 'defends', 'pages-es'],
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
        'ASCIIDOC_OPTIONS': ['-f /etc/asciidoc/lang-es.conf', '-a icons',
                             '-a iconsdir=/web/es/images/icons',
                             '-a tooltip=/web/es/images/icons/tooltip.png'],
    }
}
SUBSITE_LANG = {
     'en': 'https://fluidattacks.com/web/en',
     'es': 'https://fluidattacks.com/web/es',
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
