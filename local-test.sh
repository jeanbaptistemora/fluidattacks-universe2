#!/usr/bin/env bash
set -e

echo "Deploying FLUID Website (local environment)"
cd /web

echo "Removing older builds (1/4) . . ."
rm -rf ./output

echo "Generating build (2/4) . . ."

# Change production to local environment
sed -i 's/https:\/\/fluidattacks.com/http:\/\/localhost:8000/' pelicanconf.py

# Compile dictionaries for subsites in english and spanish
pybabel compile --directory theme/2014/translations --domain messages

# Generate static site
pelican --fatal errors --fatal warnings content/

# Remove unused folder created for the default language (de)
rm -rf output/web/de

# Copy static files (images, code, ...) to the folder of the respective .html article
mv output/web/en/blog-en/* output/web/en/blog && mv output/web/es/blog-es/* output/web/es/blog

echo "Updating sitemap, setting redirect and pages images (3/4) . . ."

# Merge sitemaps from both subsites and the domain path in a single file
./xmlcombine.sh

# Copy static files (images, code, ...) to the folder of the respective .html page
cp -r output/web/es/pages-es*/* output/web/es/ && rm -rf output/web/es/pages-es*
cp -r output/web/en/pages-en*/* output/web/en/ && rm -rf output/web/en/pages-en*

# Set redirect from /web to /web/en/
mv output/web/en/redirect/index.html output/web/ && rmdir output/web/en/redirect/

# Set robots.txt file
cp robots.txt output/web/

# Organize images of articles with draft status
./draft.sh

# Undo changes made to the file and change permissions of the files used by the container as root
git checkout -- pelicanconf.py
chmod -R a+rwX {output/,pelicanconf.py,cache/}
rm ./*.pyc

echo "Starting local HTTP server on port 8000 (4/4) . . ."
cd ./output
python -m SimpleHTTPServer
