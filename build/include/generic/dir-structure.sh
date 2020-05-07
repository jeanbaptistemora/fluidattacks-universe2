# shellcheck shell=bash

# base directory with write permissions
mkdir root

# where repository files will be placed
mkdir root/src
mkdir root/src/repo

# where pip cache dir and python site-packages will be stored
mkdir root/python
mkdir root/python/cache-dir
mkdir root/python/site-packages

# where turtle shell will be stored
mkdir root/.turtle

# where ruby gems will be stored
mkdir root/gems

# where Go packages will be stored
mkdir root/go
