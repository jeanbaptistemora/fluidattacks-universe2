GC='\033[0;32m'
NC='\033[0m'

ERRORS=0

for FILE in $(find output -iname '*.html');do
  sed -i 's/<span\ class=".\{1,3\}"><\/span>//g' $FILE
  echo -e ${GC}$FILE${NC};
  if ! tidy -e -q $FILE;then
    ERRORS=1;
  fi;
done;

if [ "$ERRORS" = "0" ];then
  echo -e "${GC}Los HTML generados cumplen con los estándares para HTML5${NC}";
fi;

exit $ERRORS
