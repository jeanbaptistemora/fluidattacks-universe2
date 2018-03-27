# Define green, red and no color
RD='\033[0;31m'
GC='\033[0;32m'
NC='\033[0m'
ERRORS=0

#For spanish blog / defends
for FILE in $(find content/blog-es content/defends -iname '*.adoc'); do

# Check that every article in blog and defends has a valid category
  ARTCAT=$(cat $FILE | pcregrep --color -o '(?<=^:category:).*');
  if ! cat categorias.lst | pcregrep -q $ARTCAT ; then
   echo -e "${RD} $ARTCAT";
  echo -e "${GC} The article does not match any valid category. Please correct the file \"$FILE\"${NC}";
  ERRORS=1;
  fi

# Check that every article in blog has valid tags
  if ! pcregrep -q ':defends:' $FILE ; then
    ARTTAGS=$(cat $FILE | pcregrep -o '(?<=^:tags:).*'| tr , \\n)
    for TAG in $( echo $ARTTAGS ); do
      if ! cat etiquetas.lst | pcregrep -q $TAG ; then
        echo -e "${RD} $TAG";
      echo -e "${GC} The previous tag is not valid. Please correct the file \"$FILE\" or add the new tag in the list. ${NC}";
      ERRORS=1;
      fi
    done
  fi
done

#For english blog
for FILE in $(find content/blog-en -iname '*.adoc'); do

# Check that every article in blog has a valid category
  ARTCAT=$(cat $FILE | pcregrep --color -o '(?<=^:category:).*');
  if ! cat categories.lst | pcregrep -q $ARTCAT ; then
  echo -e "${RD} $ARTCAT";
  echo -e "${GC} The article does not match any valid category. Please correct the file \"$FILE\"${NC}";
  ERRORS=1;
  fi

# Check that every article in blog has valid tags
  ARTTAGS=$(cat $FILE | pcregrep -o '(?<=^:tags:).*'| tr , \\n)
    for TAG in $( echo $ARTTAGS ); do
      if ! cat tags.lst | pcregrep -q $TAG ; then
        echo -e "${RD} $TAG";
      echo -e "${GC} The previous tag is not valid. Please correct the file \"$FILE\" or add the new tag in the list. ${NC}";
      ERRORS=1;
      fi
    done

done

exit $ERRORS
