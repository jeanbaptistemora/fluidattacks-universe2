#!/usr/bin/env bash

# This script aims to normalize the categories and tags used in blog articles
# according to a predefined set, in order to better classify related articles
# and have a more organized and condensed database.

# Define green, red and no color
RD='\033[0;31m'
GC='\033[0;32m'
NC='\033[0m'
ERRORS=0

#For defends
while IFS= read -r FILE; do
# Check that every article in blog and defends has a valid category
  ARTCAT=$(pcregrep --color -o '(?<=^:category:\s).*' "$FILE");
  if ! pcregrep -q "$ARTCAT" categorias.lst; then
    echo -e "${RD}$ARTCAT";
    echo -e "${GC}The article does not match any valid category. Please correct the file \"$FILE\"${NC}";
    ERRORS=1;
  fi
done < <(find content/defends -iname '*.adoc')


#For spanish blog
while IFS= read -r FILE; do

# Check that every article in blog and defends has a valid category
  ARTCAT=$(pcregrep --color -o '(?<=^:category:\s).*' "$FILE");
  if ! pcregrep -q "$ARTCAT" categorias.lst; then
    echo -e "${RD}$ARTCAT";
    echo -e "${GC}The article does not match any valid category. Please correct the file \"$FILE\"${NC}";
    ERRORS=1;
  fi

# Check that every article in blog has valid tags
    ARTTAGS=$(pcregrep -o '(?<=^:tags:\s).*' "$FILE" | sed 's/,\ /\n/g')
    while IFS= read -r TAG; do
      if ! pcregrep -q "$TAG" etiquetas.lst; then
        echo -e "${RD}$TAG";
        echo -e "${GC}The previous tag is not valid. Please correct the file \"$FILE\" or add the new tag in the list. ${NC}";
        ERRORS=1;
      fi
    done < <(echo "$ARTTAGS")

#Check that every article in blog has a valid title lenght
  if pcregrep -o '(?<=^=\s).{37,}' "$FILE"; then
    echo -e "${GC}The title lenght exceeds 35 characters. Please correct the file \"$FILE\"${NC}"
    ERRORS=1;
  fi

#Check that every article in blog has a subtitle defined
  if ! pcregrep -q '^:subtitle:' "$FILE"; then
    echo -e "${GC}The attribute \"subtitle\" must be defined in every .adoc. Please correct the file \"$FILE\"${NC}"
    ERRORS=1;
  fi

#Check that every article in blog has a valid subtitle lenght
  if pcregrep -o '(?<=^:subtitle: ).{56,}' "$FILE"; then
    echo -e "${GC}The subtitle lenght exceeds 55 characters. Please correct the file \"$FILE\"${NC}"
    ERRORS=1;
  fi

done < <(find content/blog-es -iname '*.adoc')

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

#Check that every article in blog has a valid title lenght
  if pcregrep -o '(?<=^=\s).{37,}' "$FILE"; then
    echo -e "${GC}The title lenght exceeds 35 characters. Please correct the file \"$FILE\"${NC}"
    ERRORS=1;
  fi

#Check that every article in blog has a subtitle defined
  if ! pcregrep -q '^:subtitle:' "$FILE"; then
    echo -e "${GC}The attribute \"subtitle\" must be defined in every .adoc. Please correct the file \"$FILE\"${NC}"
    ERRORS=1;
  fi

#Check that every article in blog has a valid subtitle lenght
  if pcregrep -o '(?<=^:subtitle: ).{56,}' "$FILE"; then
    echo -e "${GC}The subtitle lenght exceeds 55 characters. Please correct the file \"$FILE\"${NC}"
    ERRORS=1;
  fi

done < <(find content/blog-en -iname '*.adoc')

exit $ERRORS
