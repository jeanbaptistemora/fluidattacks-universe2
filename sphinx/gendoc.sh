#!/usr/bin/env sh

striprun() {
    asserts "$1" |
    perl -pe 's/\e([^\[\]]|\[.*?[a-zA-Z]|\].*?\a)//g' |
    tee "$1".out
}

# Execute the examples and save their output
for example in sphinx/source/example/*.py; do
  striprun "$example"
done

# HTML must go to public/ for gitlab pages
mkdir -p public/
# Generate e: separate page per module f: overwrite M: module doc first
sphinx-apidoc -efM fluidasserts -o sphinx/source
# Get version from build/dist zip
VER=$(find /builds/fluidsignal/asserts/build/dist/ -type f -printf '%f' | \
      sed 's_fluidasserts-\|.zip__g')
CHECKS=$(grep -rIE '@(track|api)' fluidasserts/ | wc -l)
sed -i "s/<CHECKS>/$CHECKS/" sphinx/source/index.rst
sphinx-build -D version="v.$VER" -D release="v.$VER" \
             -b dirhtml -a sphinx/source/ public/
sphinx-build -b linkcheck sphinx/source public/review/
sphinx-build -b coverage  sphinx/source public/review/
