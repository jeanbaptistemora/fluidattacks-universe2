#!/usr/bin/env bash
set -e

pybabel compile --directory theme/2014/translations --domain messages
pelican --fatal errors --fatal warnings content/

rm -rf output/web/de
mv output/web/pages/* output/web/
rmdir output/web/pages

cp sitemap.xml output/sitemap.xml
tail -n +6 output/web/sitemap.xml >> output/sitemap.xml
sed -i '/<url>/{:a;N;/<\/url>/!ba};/blog\/\(authors\|tags\|categories\)/d' output/sitemap.xml
sed -i '/^$/d' output/sitemap.xml
rm output/web/sitemap.xml

cp robots.txt output/robots.txt
