# Define green color and no color
GC='\033[0;32m'
NC='\033[0m'
ERRORS=0

# Search for incorrect names
if pcregrep --color -nr --include='\.adoc' -e 'Fluid|Fluidsignal\ Group|fluidsignal' content; then echo -e "${GC}\nEl único nombre aceptado es FLUID${NC}"; ERRORS=1; fi

# Leave a blank space after a title
if pcregrep --color -Mrn --include='\.adoc' '^=.*.[A-Z].*.*\n.*[A-Z]' content ; then echo -e "${GC}\nDejar un espacio en blanco luego de títulos${NC}"; ERRORS=1; fi

# Check numerated references
if pcregrep --color -Mnr '^== Referenc.*.*\n.*\n[A-Za-z]' content; then echo -e "${GC}\nERRORES: Referencias deben ser numeradas${NC}"; ERRORS=1;fi

# solo hace match de enlaces en viñetas de una sola línea, pero es un gran avance.  Pendiente enlaces en medio del texto
# if grep -P -n -r --include "*.adoc" '^. https+://.*[^\]]$' content; then echo 'ERRORES: Enlaces deben tener "[Titulo]".'; ERRORS=1;fi

# Check there are not any articles with the .asc extension
if find content -iname '*.asc' | egrep '.*'; then echo -e "${GC}ERRORES: Extension \"asc\" no soportada.${NC}"; ERRORS=1;fi

# Check that names do not have underscore
if find content -iname '*_*' | egrep '.*'; then echo -e "${ 	GC}ERRORES: Usar guión alto '-' en vez de guión bajo '_'.${NC}"; ERRORS=1;fi

# Check every image is in PNG format
if find content -iname '*.jpg' | egrep '.*'; then echo -e "${GC}ERRORES: Formato de imagenes debe ser \"png\".${NC}"; ERRORS=1;fi

# Check no uppercase characters are used in the names of the files
if find content | egrep '.*[A-Z].*'; then echo -e "${GC}ERRORES: Rutas siempre en minuscula${NC}"; ERRORS=1;fi

# Check that files names do not have spaces in them
if find content -iname '* *' | egrep '.*'; then echo -e "${GC}ERRORES: Rutas sin espacio. Usar guión alto \"-\".${NC}"; ERRORS=1;fi

# slugs más largos de 50 + raíz superan requisito de URL<=76
if grep -E -n -r --include "*.adoc" "^:slug: .{50,}" content; then echo 'ERRORES: URL debe ser de máximo 76 caracteres.'; ERRORS=1;fi

# Check that 4 - delimit the code block, not more, not less
if  pcregrep --color -nr --include='\.adoc' '^-{5,}' content; then echo -e "${GC}ERRORES: Delimitador de bloque debe ser 4 exactamente.${NC}"; ERRORS=1;fi

# Check that the start attribute is never used
if pcregrep --color -nr --include='\.adoc' '\[start' content; then echo -e "${GC}ERRORES: No usar el atributo \"start\" para la enumeración de listas. Utilizar el caracter '+' para concatenar el contenido de cada numeral${NC}"; ERRORS=1;fi

# Check that the slug ends in a '/'
if pcregrep --color -nr --include='\.adoc' 'slug:.*[a-z]$' content; then echo -e "${GC}ERRORES: El \"slug\" del artículo debe terminar en '/'${NC}"; ERRORS=1;fi

# requiere pcregrep para busqueda multilinea
# if pcregrep -M -n -r --include='\.adoc$' '^\[source,.*\n[^.].*\n[^-]' content; then echo 'ERRORES: Source sin caption de archivo ".file.py (parte a)" y delimitadores "----".'; ERRORS=1;fi

# Check alternative text in images
if pcregrep --color -Mnr --include='\.adoc' '^image\:\:.*\[\]' content; then echo -e "${GC}ERRORES: Imagenes sin texto alternativo.${NC}"; ERRORS=1;fi

# Check doble titulo principal
if pcregrep -M -n -r --include='\.adoc$' '^= .*\n\n.*^= .*\n\n' content; then echo 'ERRORES: Doble titulo principal.'; ERRORS=1;fi

# Check double quotes are not used in the title
if pcregrep --color -nr --include='\.adoc' '^= [A-Z].*\"' content; then echo -e "${GC}ERRORES: No usar comillas dobles \" en el título.${NC}"; ERRORS=1;fi

exit $ERRORS
