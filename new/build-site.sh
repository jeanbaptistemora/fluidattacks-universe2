#!/usr/bin/env bash
set -e

echo '[INFO] Compiling New site'
pybabel compile --directory theme/2020/translations --domain messages
pelican --fatal errors --fatal warnings content/
echo '[INFO] Finished compiling New site'

rm -rf output/web
mv output/newweb/pages/* output/newweb/
rmdir output/newweb/pages

cp ../sitemap.xml output/sitemap.xml
tail -n +6 output/newweb/sitemap.xml >> output/sitemap.xml
sed -i '/<url>/{:a;N;/<\/url>/!ba};/blog\/\(authors\|tags\|categories\)/d' output/sitemap.xml
sed -i '/^$/d' output/sitemap.xml
rm output/newweb/sitemap.xml

cp ../robots.txt output/robots.txt
