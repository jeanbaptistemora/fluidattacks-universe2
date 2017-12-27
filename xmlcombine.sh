#!/bin/bash
cp sitemap.xml output/sitemap.xml
tail -n +6 output/en/sitemap.xml | head -n -1 >> output/sitemap.xml
tail -n +6 output/es/sitemap.xml >> output/sitemap.xml
rm {output/en/sitemap.xml,output/es/sitemap.xml}
