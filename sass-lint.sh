GC='\033[0;32m'
NC='\033[0m'

ERRORS=0

for FILE in $(find theme -type f \( -name '*.sass' -or -name '*.scss' \));do
  echo -e ${GC}$FILE${NC};
  if ! sass-lint.js -q -v --max-warnings 0 $FILE;then
    ERRORS=1;
  fi;
done;

if [ "$ERRORS" = "0" ];then
  echo -e "${GC}Los archivos SASS cumplen con todas las reglas del linter${NC}";
fi;

exit $ERRORS
