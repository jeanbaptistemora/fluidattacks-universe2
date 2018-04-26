#!/usr/bin/env bash

# This script set a strict spelling for certain words and validates
# the correct spelling  in all content folders.
# To add new rules simply add the correct spelling
# in the file strict-words.lst

GC='\033[0;32m'
NC='\033[0m'
ERRORS=0

while IFS= read -r CORRECT; do
  while IFS= read -r FILE; do
    # Check if strict spelling has 2 words
    if [[ "$CORRECT" =~ \   ]]; then
      SRCH=${CORRECT// /(\\s)?}
    else
      SRCH=$CORRECT
    fi

    if  ./exttxt.sh "$FILE" | pcregrep -ioqM "$SRCH"; then

      CURRENT=$(./exttxt.sh "$FILE" | pcregrep -ioM '(\s|^)[\*|\+|\(]?'"$SRCH"'[\*\+\)]?[\.\:\;\,]?(\s|\n|\])' | pcregrep -ioM "$SRCH" )

      while IFS=$'\n' read -r WORD; do
        if  [[ "$WORD" != "$CORRECT" ]]; then
          VALIDATE=$(./exttxt.sh "$FILE" | pcregrep "$WORD")
            if [[ "$VALIDATE" =~ $WORD ]]; then
              echo -e "$VALIDATE" | grep -E --color "$WORD"
              echo -e "${GC}The spelling $WORD is invalid, the only admitted spelling is $CORRECT. Please correct the file \"$FILE\"${NC}"
              ERRORS=1;
            fi
        fi
      done < <(echo -e "$CURRENT\\n"|grep -v "^$")
    fi

  done < <(find content -iname '*.adoc')
done < strict-words.lst

exit $ERRORS
