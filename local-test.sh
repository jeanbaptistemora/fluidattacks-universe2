#!/usr/bin/env bash

# This script deploys the website locally through a simple server.
# It allows the developer to review the changes introduced and
# avoid unexpected behaviour in the site.

set -e

echo "Deploying FLUID Website (local environment)"
cd /web

echo "Removing older builds (1/5) . . ."
rm -rf ./output

echo "Generating build (2/5) . . ."

# Change production to local environment
sed -i 's|https://fluidattacks.com|http://localhost:8000|g' pelicanconf.py

echo "Compiling TS files (3/5) . . ."
npm run --prefix deploy/builder/ lint
npm run --prefix deploy/builder/ build
./build-site.sh

# Undo changes made to the file and change permissions of the files used by the container as root
git checkout -- pelicanconf.py
chmod -R a+rwX {output/,pelicanconf.py,cache/}
rm ./*.pyc

echo "Starting local HTTP server on port 8000 (5/5) . . ."
cd ./output
python -m SimpleHTTPServer
