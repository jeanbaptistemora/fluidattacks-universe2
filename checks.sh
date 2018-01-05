# Define green color and no color
GC='\033[0;	32m'
NC='\033[0m'
ERRORS=0

# Search for incorrect names
if pcregrep --color -nr --include='\.adoc' -e 'Fluid|Fluidsignal\ Group|fluidsignal' content/; then echo -e "${GC}\nEl único nombre aceptado es FLUID${NC}"; ERRORS=1; fi

# Leave a blank space after a title
if pcregrep --color -Mrn --include='\.adoc' '^=.*.*\n.*[A-Z0-9]' content/; then echo -e "${GC}\nDejar un espacio en blanco luego de títulos${NC}"; ERRORS=1; fi

#if pcregrep --color -Mnr '^\nhttp' content/kb/; then echo -e "${GC}\nERRORES: Referencias deben ser numeradas${NC}"; exit 1;fi

# solo hace match de enlaces en viñetas de una sola línea, pero es un gran avance.  Pendiente enlaces en medio del texto
# if grep -P -n -r --include "*.adoc" '^. https+://.*[^\]]$' content; then echo 'ERRORES: Enlaces deben tener "[Titulo]".'; exit 1;fi

# if find content -iname '*.asc' | egrep '.*'; then echo 'ERRORES: Extension "asc" no soportada.'; exit 1;fi

# if find content -iname '*_*' | egrep '.*'; then echo 'ERRORES: Usar guión alto "-" en vez de guion bajo "_".'; exit 1;fi

# if find content -iname '*.jpg' | egrep '.*'; then echo 'ERRORES: Formato de imagenes debe ser "png".'; exit 1;fi

# if find content | egrep '.*[A-Z].*'; then echo 'ERRORES: Rutas siempre en minuscula'; exit 1;fi

# if find content -iname '* *' | egrep '.*'; then echo 'ERRORES: Rutas sin espacio. Usar guión alto "-".'; exit 1;fi

# slugs más largos de 50 + raíz superan requisito de URL<=76
# if grep -E -n -r --include "*.adoc" "^:slug: .{50,}" content; then echo 'ERRORES: URL debe ser de máximo 76 caracteres.'; exit 1;fi

# if grep -E -n -r --include "*.adoc" "^-{5,}" content; then echo 'ERRORES: Delimitador de bloque debe ser 4 exactamente.'; exit 1;fi

# requiere pcregrep para busqueda multilinea
# if pcregrep -M -n -r --include='\.adoc$' '^\[source,.*\n[^.].*\n[^-]' content; then echo 'ERRORES: Source sin caption de archivo ".file.py (parte a)" y delimitadores "----".'; exit 1;fi

# if pcregrep -M -n -r --include='\.adoc$' '^image\:\:.*\[\]' content; then echo 'ERRORES: Imagenes sin texto alternativo.'; exit 1;fi

# if pcregrep -M -n -r --include='\.adoc$' '^= .*\n\n.*^= .*\n\n' content; then echo 'ERRORES: Doble titulo principal.'; return 1;fi

exit $ERRORS
