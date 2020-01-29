# shellcheck shell=bash

# base directory with write permissions
mkdir root

# where repository files will be placed
mkdir root/src
mkdir root/src/repo

# where pip's cache dir and python's site-packages will live
mkdir root/python
mkdir root/python/cache-dir
mkdir root/python/site-packages
