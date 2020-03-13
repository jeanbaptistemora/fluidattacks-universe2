#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

# Site information
AUTHOR = 'Fluid Attacks'

# Theme
THEME = 'theme/2020/'

# Date and time configuration
TIMEZONE = 'America/Bogota'
DEFAULT_DATE_FORMAT = ('%Y-%m-%d')
DEFAULT_LANG = 'de'
OUTPUT_PATH = 'output/web/de'

# URLs format
PATH = 'content'
ARTICLE_PATHS = ['blog-de']
PAGE_PATHS = ['pages-de']
PAGE_URL = '{slug}'
PAGE_SAVE_AS = 'pages/{slug}index.html'
USE_FOLDER_AS_CATEGORY = False
LANDING_SAVE_AS = 'index.html'

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
           'tag_cloud'
]
RELATED_POSTS_MAX = 3
DIRECT_TEMPLATES = ['landing']
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
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n', 'jinja2.ext.do']}
I18N_SUBSITES = {
    'en': {
        'SITENAME': 'A Pentesting Company | Fluid Attacks',
        'SITEURL': 'https://fluidattacks.com/newweb',
        'OUTPUT_PATH': 'output/newweb',
        'THEME': 'theme/2020/',
        'ARTICLE_PATHS': ['blog'],
        'PAGE_PATHS': ['pages'],
        'PAGE_SAVE_AS': 'pages/{slug}index.html',
        'ARTICLE_SAVE_AS': 'blog/{slug}index.html',
        'STATIC_PATHS': ['files', 'images', 'blog', 'pages'],
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
        'ASCIIDOC_OPTIONS': ['-a icons', '-a iconsdir=/web/images/icons',
                             '-a tooltip=/web/images/icons/tooltip.png'],
    },
}
SUBSITE_LANG = {
     'en': 'https://fluidattacks.com/newweb',
}
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
DISQUS_SITENAME = 'fluidattacks'

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
