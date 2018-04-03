#!/usr/bin/env bash

# This script locates all the generated HTML files and runs the linter
# Tidy-HTML against them, so the content served fulfills the HTML standards.

GC='\033[0;32m'
NC='\033[0m'

ERRORS=0

while IFS= read -r FILE;do
  # Erase empty span tags created by Pygments (known and accepted issue)
  sed -i 's/<span\ class=".\{1,3\}"><\/span>//g' "$FILE"
  echo -e "${GC}$FILE${NC}";
  # Run Tidy-HTML against the generagted files
  if ! tidy -e -q "$FILE";then
    ERRORS=1;
  fi;
done < <(find output -iname '*.html')

if [ "$ERRORS" = "0" ];then
  echo -e "${GC}Los HTML generados cumplen con los estándares para HTML5${NC}";
fi;

exit $ERRORS
