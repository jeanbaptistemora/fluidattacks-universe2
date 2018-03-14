# Define green, red and no color
RD='\033[0;31m'
GC='\033[0;32m'
NC='\033[0m'
ERRORS=0

for FILE in $(find content/blog-es content/blog-en content/defends -iname '*.adoc'); do
  
# Check that every article in blogs and defends has a valid category	
  ARTCAT=$(cat $FILE | pcregrep --color -o '(?<=^:category:).*');
  if ! cat categories.lst categorias.lst | pcregrep -q $ARTCAT ; then
 	echo -e "${RD} $ARTCAT";
	echo -e "${GC} The article does not match any valid category. Please correct the file \"$FILE\"${NC}";
	ERRORS=1;
  fi

# Check that every article in blogs has valid tags
  if ! pcregrep -q ':defends:' $FILE ; then 
  	ARTTAGS=$(cat $FILE | pcregrep -o '(?<=^:tags:).*'| tr , \\n)
  	for TAG in $( echo $ARTTAGS ); do
  	  if ! cat etiquetas.lst tags.lst | pcregrep -q $TAG ; then
  	  	echo -e "${RD} $TAG";
  		echo -e "${GC} The previous tag is not valid. Please correct the file \"$FILE\" or add the new tag in the list. ${NC}";
	    ERRORS=1;  	
  	  fi
  	done
  fi 

done

exit $ERRORS