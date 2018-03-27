#!/usr/bin/env bash

# Define green, red and no color
RD='\033[0;31m'
GC='\033[0;32m'
NC='\033[0m'
ERRORS=0

#For spanish blog / defends
while IFS= read -r FILE; do

# Check that every article in blog and defends has a valid category
  ARTCAT=$(pcregrep --color -o '(?<=^:category:\s).*' "$FILE");
  if ! pcregrep -q "$ARTCAT" categorias.lst; then
    echo -e "${RD}$ARTCAT";
    echo -e "${GC}The article does not match any valid category. Please correct the file \"$FILE\"${NC}";
    ERRORS=1;
  fi

# Check that every article in blog has valid tags
  if ! pcregrep -q ':defends:' "$FILE" ; then
    ARTTAGS=$(pcregrep -o '(?<=^:tags:\s).*' "$FILE" | sed 's/,\ /\n/g')
    while IFS= read -r TAG; do
      if ! pcregrep -q "$TAG" etiquetas.lst; then
        echo -e "${RD}$TAG";
        echo -e "${GC}The previous tag is not valid. Please correct the file \"$FILE\" or add the new tag in the list. ${NC}";
        ERRORS=1;
      fi
    done < <(echo "$ARTTAGS")
  fi
done < <(find content/blog-es content/defends -iname '*.adoc')

#For english blog
while IFS= read -r FILE; do

# Check that every article in blog has a valid category
  ARTCAT=$(pcregrep --color -o '(?<=^:category:\s).*' "$FILE");
  if ! pcregrep -q "$ARTCAT" categories.lst; then
  echo -e "${RD}$ARTCAT";
  echo -e "${GC}The article does not match any valid category. Please correct the file \"$FILE\"${NC}";
  ERRORS=1;
  fi

# Check that every article in blog has valid tags
  ARTTAGS=$(pcregrep -o '(?<=^:tags:\s).*' "$FILE" | sed 's/,\ /\n/g')
    while IFS= read -r TAG; do
      if ! pcregrep -q "$TAG" tags.lst; then
        echo -e "${RD}$TAG";
        echo -e "${GC}The previous tag is not valid. Please correct the file \"$FILE\" or add the new tag in the list. ${NC}";
        ERRORS=1;
      fi
    done < <(echo "$ARTTAGS")

done < <(find content/blog-en -iname '*.adoc')

exit $ERRORS
