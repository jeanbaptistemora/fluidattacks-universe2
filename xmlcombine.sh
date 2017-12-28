#!/bin/bash
cp sitemap.xml output/web/sitemap.xml
tail -n +6 output/web/en/sitemap.xml | head -n -1 >> output/web/sitemap.xml
tail -n +6 output/web/es/sitemap.xml >> output/web/sitemap.xml
rm {output/web/en/sitemap.xml,output/web/es/sitemap.xml}
