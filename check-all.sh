# Define green color and no color
GC='\033[0;32m'
NC='\033[0m'
ERRORS=0

# Check use of incorrect names to address the company
if pcregrep --color -nr --include='\.adoc' -e 'Fluid|Fluidsignal\ Group|fluidsignal|\ fluid[)}\ \]]' content; then
  echo -e "${GC}\nThe only accepted name is FLUID.${NC}"
  ERRORS=1;
fi

# Check blank spaces after headers
if pcregrep --color -Mrn --include='\.adoc' '^=.*.[A-Z].*.*\n.*[A-Z]' content ; then
  echo -e "${GC}\nLeave a blank space after a header.${NC}"
  ERRORS=1;
fi

# Check that the references are numerated
if pcregrep --color -Mnr '^== Referenc.*.*\n.*\n[A-Za-z]' content; then
  echo -e "${GC}\nReferences must be numbered.${NC}"
  ERRORS=1;
fi

# Check there are not any articles with the .asc extension
if find content -iname '*.asc' | egrep '.*'; then
  echo -e "${GC}Extension \".asc\" not supported.${NC}"
  ERRORS=1;
fi

# Check that names do not have underscore
if find content -iname '*_*' | egrep '.*'; then
  echo -e "${GC}Use hyphen '-' instead of underscore '_' for filenames.${NC}"
  ERRORS=1;
fi

# Check every image is in PNG format
if find . -name '*.jpg' -o -name '*.jpeg' -o -name '*.svg' | egrep '.*'; then
  echo -e "${GC}Image format must be \"png\".${NC}"
  ERRORS=1;
fi

# Check every image fits the size limit
if find . -name '*.png' -size +300k | egrep '.*'; then
  echo -e "${GC}Images cannot have a size over 300kB.${NC}"
  ERRORS=1;
fi

# Check that the image caption is not manually placed
if pcregrep --color -nr --include='\.adoc' -e '^\.Imagen?\ [0-9]|^\.Figur(a|e)\ [0-9]' content; then
  echo -e "${GC}Images must not have the words \"Image #\" or \"Figure #\" in their captions.${NC}"
  ERRORS=1;
fi

# Check the titles of the images are well placed
if pcregrep --color -Mnr --include='\.adoc' 'image::.*\n\.[a-zA-Z]' content; then
  echo -e "${GC}Image captions are placed after the image, not before.${NC}"
  ERRORS=1;
fi

# Check no uppercase characters are used in the filenames
if find content | egrep '.*[A-Z].*'; then
  echo -e "${GC}Filenames must always be lowercase.${NC}"
  ERRORS=1;
fi

# Check that filenames do not have spaces in them
if find content -iname '* *' | egrep '.*'; then
  echo -e "${GC}Filenames must not have spaces in them, use hyphen \"-\" instead.${NC}"
  ERRORS=1;
fi

# Check that slugs have under 44 characters
if grep -E -n -r --include "*.adoc" "^:slug: .{44,}" content; then
  echo -e "${GC}The \"slug\" can have 43 characters maximum.${NC}"
  ERRORS=1;
fi

# Check that 4 '-' delimit the code block, not more, not less
if  pcregrep --color -nr --include='\.adoc' '^-{5,}' content; then
  echo -e "${GC}Code blocks must be delimited by exactly four hyphens '-'.${NC}"
  ERRORS=1;
fi

# Check that the start attribute is never used
if pcregrep --color -nr --include='\.adoc' '\[start' content; then
  echo -e "${GC}Do not use the \"start\" attribute for list numbering, use a plus sing '+' to concatenate the content that breaks the numbering.${NC}"
  ERRORS=1;
fi

# Check that the slug ends in a '/'
if pcregrep --color -nr --include='\.adoc' '^:slug:.*[a-z]$' content; then
  echo -e "${GC}The \"slug\" must end in '/'.${NC}"
  ERRORS=1;
fi

# Check alternative text in images
if pcregrep --color -Mnr --include='\.adoc' 'image\:\:.*\[\]' content; then
  echo -e "${GC}Images do not have alt attribute.${NC}"
  ERRORS=1;
fi

# Check double main title
if pcregrep -M -n -r --include='\.adoc$' '^= .*\n\n.*^= .*\n\n' content; then
  echo -e "${GC}Double main title.${NC}"
  ERRORS=1;
fi

# Check double quotes are not used in the title
if pcregrep --color -nr --include='\.adoc' '^= [A-Z].*\"' content; then
  echo -e "${GC}Do not use double quotes \" in the title.${NC}"
  ERRORS=1;
fi

# Check that blog articles have alt description for their featured images
if pcregrep --color -Lnr --include='\.adoc' '^:alt:.*' content/blog*; then
  echo -e "${GC}The articles must have the metadata \"alt\" set for their representative image.${NC}"
  ERRORS=1;
fi

# Check that code does not follow inmmediatly after a paragraph in the KB
if pcregrep --color -Mnr --include='\.adoc' '^[a-zA-Z0-9].*\n.*\[source' content/defends; then
  echo -e "${GC}Source codes must be separated from a paragraph using a plus sign '+'.${NC}"
  ERRORS=1;
fi

# Check that the title of the website does not have more than 60 characters (Once "| FLUID" is attached)
if pcregrep --color -nru --include='\.adoc' '^= [A-Z¿¡].{52}' content; then
  echo -e "${GC}Titles can have 52 characters maximum.${NC}"
  ERRORS=1;
fi

# Check that every .adoc has keywords defined
if pcregrep -Lnr --include='\.adoc' ':keywords:' content; then
  echo -e "${GC}The attribute \"keywords\" must be defined in every .adoc.${NC}"
  ERRORS=1;
fi

# Check that the every .adoc has description defined
if pcregrep -Lnr --include='\.adoc' ':description:' content; then
  echo -e "${GC}The attribute \"description\" must be defined in every .adoc.${NC}"
  ERRORS=1;
fi

# Check that the diagram names start with the word "diagram"
if pcregrep -nr '"(graphviz|plantuml)",\s?"(?!diagram).*\.png' content; then
  echo -e "${GC}The name of the diagrams must start with the word \"diagram\".${NC}";
  ERRORS=1;
fi

# Check that translation names finish with '/'
if pcregrep --color -nr --include='\.adoc' '^:translate.*(?<!/)$' content; then
  echo -e "${GC}The name of the translated file must end in '/'.${NC}";
  ERRORS=1;
fi

# Check all Asciidoc metadata are lowercase
if pcregrep --color -nr --include='\.adoc' '^:[A-Z]' content; then
  echo -e "${GC}All metadata attributes in asciidoc files must be lowercase.${NC}"
  ERRORS=1;
fi

# Check the character '>' is not used in type button links
if pcregrep --color -nr --include='\.adoc' '\[button\].*>' content; then
  echo -e "${GC}The '>>' characters are written by the style and are not needed in the source code.${NC}"
  ERRORS=1;
fi

# Check that the meta description has a minimum lenght of 250 characters and a maximum length of 300 characters
for FILE in $(find content -iname '*.adoc'); do
  if cat $FILE | pcregrep --color -no '(?<=:description: ).{307,}$|(?<=:description: ).{0,249}$'; then
    echo -e "${GC}Descriptions must be in the [250-300] characters range. The previous description belongs to the file \"$FILE\".${NC}";
    ERRORS=1;
  fi

# Check if there are exactly 6 keywords
  NUMKEYWS=$(cat $FILE | pcregrep -no '(?<=^:keywords:).*' | tr , \\n | wc -l)
  if [ $NUMKEYWS -ne 6 ]; then
    cat $FILE | pcregrep --color -no '(?<=^:keywords:).*';
    echo -e "${GC}There must be exactly 6 keywords. Please correct the file \"$FILE\".${NC}";
    ERRORS=1;
  fi

#Check that every URL starts with link:
  if sh exttxt.sh $FILE | pcregrep --color -n '(\s|\w|\()http(s)?://'; then
    echo -e "${GC}URLs must start with 'link:'. Please correct the file \"$FILE\".${NC}";
    ERRORS=1;
  fi

#Check that every URL has a short name between brackets:
  if sh exttxt.sh $FILE | pcregrep --color -n 'link:http(s)?://'; then
    echo -e "${GC}URLs must have a short name between brackets. Please correct the file \"$FILE\".${NC}";
    ERRORS=1;
  fi

#Check that local URLs always uses relative paths:
  if cat $FILE | pcregrep --color -n 'http(s)?://fluidattacks.com/web'; then
    echo -e "${GC}Local URLs must use relative paths. Please correct the file \"$FILE\".${NC}";
    ERRORS=1;
  fi

# Check if first source code has title
  if pcregrep --color -Mnq '^\[source' $FILE; then
    if ! pcregrep --color -Mnq '^\..*\n\[source' $FILE; then
      echo -e "${GC}The first code block of an article must have a title.${NC}";
      ERRORS=1;
    fi
  fi
done

exit $ERRORS
