# Define green, red and no color
RD='\033[0;31m'
GC='\033[0;32m'
NC='\033[0m'
ERRORS=0

for FILE in $(find content/blog-es content/blog-en -iname '*.adoc'); do

# Check that every article in blogs has a valid category	
  ARTCAT=$(cat $FILE | pcregrep --color -o '(?<=^:category:).*');
  if ! cat categories.lst categorias.lst | pcregrep -q $ARTCAT ; then
 	echo -e "${RD} $ARTCAT";
	echo -e "${GC} The article does not match any valid category. Please correct the file \"$FILE\"${NC}";
	ERRORS=1;
  fi
done

exit $ERRORS