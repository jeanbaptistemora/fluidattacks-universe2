# Define green color and no color
GC='\033[0;32m'
NC='\033[0m'
ERRORS=0

# Search for incorrect names
if pcregrep --color -nr --include='\.adoc' -e 'Fluid|Fluidsignal\ Group|fluidsignal|\ fluid[)}\ \]]' content; then echo -e "${GC}\nEl único nombre aceptado es FLUID${NC}"; ERRORS=1; fi

# Leave a blank space after a title
if pcregrep --color -Mrn --include='\.adoc' '^=.*.[A-Z].*.*\n.*[A-Z]' content ; then echo -e "${GC}\nDejar un espacio en blanco luego de títulos${NC}"; ERRORS=1; fi

# Check numerated references
if pcregrep --color -Mnr '^== Referenc.*.*\n.*\n[A-Za-z]' content; then echo -e "${GC}\nERRORES: Referencias deben ser numeradas${NC}"; ERRORS=1;fi

# solo hace match de enlaces en viñetas de una sola línea, pero es un gran avance.  Pendiente enlaces en medio del texto
# if grep -P -n -r --include "*.adoc" '^. https+://.*[^\]]$' content; then echo 'ERRORES: Enlaces deben tener "[Titulo]".'; ERRORS=1;fi

# Check there are not any articles with the .asc extension
if find content -iname '*.asc' | egrep '.*'; then echo -e "${GC}ERRORES: Extension \"asc\" no soportada.${NC}"; ERRORS=1;fi

# Check that names do not have underscore
if find content -iname '*_*' | egrep '.*'; then echo -e "${GC}ERRORES: Usar guión alto '-' en vez de guión bajo '_'.${NC}"; ERRORS=1;fi

# Check every image is in PNG format
if find . -name '*.jpg' -o -name '*.jpeg' -o -name '*.svg' | egrep '.*'; then echo -e "${GC}ERRORES: Formato de imagenes debe ser \"png\".${NC}"; ERRORS=1;fi

# Check every image fits the size limit
if find . -name '*.png' -size +300k | egrep '.*'; then echo -e "${GC}ERRORES: Las imágenes deben pesar máximo 300kB.${NC}"; ERRORS=1;fi

# Check that the image caption is not manually placed
if pcregrep --color -nr --include='\.adoc' -e '^\.Imagen?\ [0-9]|^\.Figur(a|e)\ [0-9]' content; then echo -e "${GC}ERRORES: El título de las imágenes no debe llevar caption\"Imagen #\", \"Figura #\".${NC}"; ERRORS=1;fi

# Check the titles of the images are well placed
if pcregrep --color -Mnr --include='\.adoc' 'image::.*\n\.[a-zA-Z]' content; then echo -e "${GC}ERRORES: El título de las imágenes van antes de la imagen, no después${NC}"; ERRORS=1;fi

# Check no uppercase characters are used in the names of the files
if find content | egrep '.*[A-Z].*'; then echo -e "${GC}ERRORES: Rutas siempre en minuscula${NC}"; ERRORS=1;fi

# Check that files names do not have spaces in them
if find content -iname '* *' | egrep '.*'; then echo -e "${GC}ERRORES: Rutas sin espacio. Usar guión alto \"-\".${NC}"; ERRORS=1;fi

# slugs más largos de 50 + raíz superan requisito de URL<76
if grep -E -n -r --include "*.adoc" "^:slug: .{44,}" content; then echo -e "${GC}ERRORES: El \"slug\" debe tener maximo 43 caracteres${NC}"; ERRORS=1;fi

# Check that 4 - delimit the code block, not more, not less
if  pcregrep --color -nr --include='\.adoc' '^-{5,}' content; then echo -e "${GC}ERRORES: Delimitador de bloque debe ser 4 exactamente.${NC}"; ERRORS=1;fi

# Check that the start attribute is never used
if pcregrep --color -nr --include='\.adoc' '\[start' content; then echo -e "${GC}ERRORES: No usar el atributo \"start\" para la enumeración de listas. Utilizar el caracter '+' para concatenar el contenido de cada numeral${NC}"; ERRORS=1;fi

# Check that the slug ends in a '/'
if pcregrep --color -nr --include='\.adoc' '^:slug:.*[a-z]$' content; then echo -e "${GC}ERRORES: El \"slug\" del artículo debe terminar en '/'${NC}"; ERRORS=1;fi

# requiere pcregrep para busqueda multilinea
# if pcregrep -M -n -r --include='\.adoc$' '^\[source,.*\n[^.].*\n[^-]' content; then echo 'ERRORES: Source sin caption de archivo ".file.py (parte a)" y delimitadores "----".'; ERRORS=1;fi

# Check alternative text in images
if pcregrep --color -Mnr --include='\.adoc' 'image\:\:.*\[\]' content; then echo -e "${GC}ERRORES: Imagenes sin texto alternativo.${NC}"; ERRORS=1;fi

# Check doble titulo principal
if pcregrep -M -n -r --include='\.adoc$' '^= .*\n\n.*^= .*\n\n' content; then -e echo "${GC}ERRORES: Doble titulo principal.${NC}"; ERRORS=1;fi

# Check double quotes are not used in the title
if pcregrep --color -nr --include='\.adoc' '^= [A-Z].*\"' content; then echo -e "${GC}ERRORES: No usar comillas dobles \" en el título.${NC}"; ERRORS=1;fi

# Check that blog articles have alt description for their featured images
if pcregrep --color -Lnr --include='\.adoc' '^:alt:.*' content/blog*; then echo -e "${GC}ERRORES: Los artículos deben llevar meta-descripción \"alt\" para su imagen representativa${NC}"; ERRORS=1;fi

# Check that code does not follow inmmediatly after a paragraph in the KB
if pcregrep --color -Mnr --include='\.adoc' '^[a-zA-Z0-9].*\n.*\[source' content/defends; then echo -e "${GC}ERRORES: Los bloques de código deben estar separados del párrafo por un '+'${NC}"; ERRORS=1;fi

# Check that the title of the website does not have more than 60 characters (Once "| FLUID" is attached)
if pcregrep --color -ru --include='\.adoc' '^= [A-Z¿¡].{52}' content; then echo -e "${GC}ERRORES: Los títulos deben tener máximo 52 caracteres${NC}"; ERRORS=1;fi

# Check that every .adoc has keywords defined
if pcregrep -Lr --include='\.adoc' ':keywords:' content; then echo -e "${GC}ERRORES: El atributo \":keywords:\" debe estar definido en el .adoc${NC}"; ERRORS=1;fi

# Check that the every .adoc has description defined
if pcregrep -Lr --include='\.adoc' ':description:' content; then echo -e "${GC}ERRORES: El atributo \":description:\" debe estar definido en el .adoc${NC}"; ERRORS=1;fi

# Check that the diagram names start with the word "diagram"
if pcregrep -r '"(graphviz|plantuml)",\s?"(?!diagram).*\.png' content; then
	echo -e "${GC}The name of the diagrams must start with the word \"diagram\"${NC}";
	ERRORS=1;
fi;

# Check that the meta description has a minimum lenght of 250 characters and a maximum length of 300 characters
for FILE in $(find content -iname '*.adoc'); do
  if cat $FILE | pcregrep --color -o '(?<=:description: ).{307,}$|(?<=:description: ).{0,249}$'; then
    echo -e "${GC}Descriptions must be in [250-300] characters range. The previous description belongs to the file \"$FILE\"${NC}";
    ERRORS=1;
  fi

# Check if there are exactly 6 keywords
  NUMKEYWS=$(cat $FILE | pcregrep -o '(?<=^:keywords:).*' | tr , \\n | wc -l)
  if [ $NUMKEYWS -ne 6 ]; then
  	cat $FILE | pcregrep --color -o '(?<=^:keywords:).*';
  	echo -e "${GC}There must be exactly 6 keywords. Please correct the file \"$FILE\"${NC}";
  	ERRORS=1;
  fi

# Check if first source code has title
  if pcregrep --color -Mq '^\[source' $FILE; then
    if ! pcregrep --color -Mq '^\..*\n\[source' $FILE; then
      echo -e "${GC}El primer código fuente del artículo \"$FILE\" debe llevar título.${NC}";
      ERRORS=1;	
    fi
  fi
done

exit $ERRORS
