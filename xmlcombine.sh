#!/bin/bash
# Script to generate a sitemap fiel that covers the entire website

# Main file that has the main URLs of the site predefined
cp sitemap.xml output/web/sitemap.xml

# Append all the URLs of the english subsite to the main file without the XML headers and the closing tag
tail -n +6 output/web/en/sitemap.xml | head -n -1 >> output/web/sitemap.xml

# Append all the URLs of the spanish subsite to the main file without the XML headers
tail -n +6 output/web/es/sitemap.xml >> output/web/sitemap.xml

# With the main file complete, remove the incomplete files
rm {output/web/en/sitemap.xml,output/web/es/sitemap.xml}
