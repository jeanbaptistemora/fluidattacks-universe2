#!/bin/bash
set -e

echo "Deploying FLUID Website (local environment)"
echo "Verifying content (1/5) . . ."
cd /web/content
if egrep -r 'Fluid|Fluidsignal\ Group|fluidsignal'; then echo "El único nombre aceptado es FLUID"; exit 1; fi
cd ..

echo "Removing older builds (2/5) . . ."
rm -rf ./output

echo "Generating build (3/5) . . ."
sed -i 's/https:\/\/fluid.la/http:\/\/localhost:8000/' pelicanconf.py
pelican --fatal errors content/
mv output/web/en/blog-en output/web/en/blog && mv output/web/es/blog-es output/web/es/blog

echo "Updating sitemap and setting redirect (4/5) . . ."
./xmlcombine.sh
mv output/web/en/redirect/index.html output/web/ && rmdir output/web/en/redirect/
git checkout -- pelicanconf.py
chmod -R a+rwX {output/,pelicanconf.py,pelicanconf.pyc}

echo "Starting local HTTP server on port 8000 (5/5) . . ."
cd ./output
python -m SimpleHTTPServer
