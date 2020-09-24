#!/usr/bin/env python3

"""
Pelican configuration
"""

# Site information
AUTHOR = 'Fluid Attacks'

# Theme
THEME = 'theme/2020/'

# Date and time configuration
TIMEZONE = 'America/Bogota'
DEFAULT_DATE_FORMAT = ('%Y-%m-%d')
DEFAULT_LANG = 'de'
OUTPUT_PATH = 'output/de'

# URLs format
PATH = 'content'
ARTICLE_PATHS = ['blog-de']
PAGE_PATHS = ['pages-de']
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
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = [
    'asciidoc_reader',
    'assets',
    'neighbors',
    'representative_image',
    'share_post',
    'sitemap',
    'tag_cloud',
    'tipue_search'
]
RELATED_POSTS_MAX = 3
DIRECT_TEMPLATES = [
    'error',
    'index',
    'landing',
    'authors',
    'categories',
    'tags',
    'search'
]
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
    },
    'exclude': ['blog/tags/', 'blog/categories/', 'blog/authors/']
}
DEFAULT_PAGINATION = 12
# Line that allows the localization of the site (traslation)
JINJA_ENVIRONMENT = {'extensions': ['jinja2.ext.i18n', 'jinja2.ext.do']}

SITENAME = 'A Pentesting Company | Fluid Attacks'
SITEURL = 'https://fluidattacks.com'
OUTPUT_PATH = 'output'
THEME = 'theme/2020/'
ARTICLE_PATHS = ['blog']
PAGE_PATHS = ['pages']
PAGE_SAVE_AS = 'pages/{slug}index.html'
ARTICLE_SAVE_AS = 'blog/{slug}index.html'
STATIC_PATHS = ['files', 'images', 'blog', 'pages']
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
ASCIIDOC_OPTIONS = ['-a icons', '-a iconsdir=/images/icons',
                    '-a tooltip=/images/icons/tooltip.png']

SUBSITE_LANG = {
    'en': 'fluidattacks.com',
}
ASSET_BUNDLES = (
    ('bundle', [
        'css/custom/general.scss',
        'css/custom/global.scss',
        'css/custom/custom.scss'],
     {'filters': 'scss'}),
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
