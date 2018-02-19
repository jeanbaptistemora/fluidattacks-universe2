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
sed -i 's/https:\/\/fluidattacks.com/http:\/\/localhost:8000/' pelicanconf.py
if [ ! $# -eq 0 ]; then
  sed -i 's/2014/2018/g; s/pages-en/pages-en-2018/g; s/pages-es/pages-es-2018/g' pelicanconf.py
fi

pybabel compile --directory theme/2014/translations --domain messages
pelican --fatal errors --fatal warnings content/
mv output/web/en/blog-en/* output/web/en/blog && mv output/web/es/blog-es/* output/web/es/blog

echo "Updating sitemap, setting redirect and pages images (4/5) . . ."
./xmlcombine.sh
cp -r output/web/es/pages-es*/* output/web/es/ && rm -rf output/web/es/pages-es*
cp -r output/web/en/pages-en*/* output/web/en/ && rm -rf output/web/en/pages-en*
mv output/web/en/redirect/index.html output/web/ && rmdir output/web/en/redirect/
# Undo changes made to the file and change permissions of the files used by the container as root
git checkout -- pelicanconf.py
chmod -R a+rwX {output/,pelicanconf.py,pelicanconf.pyc}

echo "Starting local HTTP server on port 8000 (5/5) . . ."
cd ./output
python -m SimpleHTTPServer
