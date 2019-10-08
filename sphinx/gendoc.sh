#!/usr/bin/env sh

striprun() {
    $1 "$2" |
    perl -pe 's/\e([^\[\]]|\[.*?[a-zA-Z]|\].*?\a)//g' |
    tee "$2".out
}

# Setup the exploits environment
mkdir -p /resources && cp {sphinx/source/example/,/}resources/secrets.yml
export yaml_key_b64='dGVzdHN0ZXN0c3Rlc3RzdGVzdHN0ZXN0c3Rlc3RzCg=='

# Execute the examples and save their output
for example in sphinx/source/example/*.py; do
  striprun "python3" "$example"
done
for example in sphinx/source/example/*.exp; do
  striprun "asserts" "$example"
done

# Generate credits.rst
echo >> sphinx/source/credits.rst

git-fame \
    -C \
    --log=ERROR \
    --silent-progress \
    --ignore-whitespace \
    --cost=cocomo \
  | grep -viE '^total [a-z]+: [0-9]+(\.[0-9]+)?$' \
  | grep -vP '^\D+?\d+\D+?0' \
  | grep -vP 'Jane Doe' \
  | tee -a sphinx/source/credits.rst

cat << EOF >> sphinx/source/credits.rst

Authors grant patrimonial and ownership rights
to Fluidsignal Group S.A.
as stated in their work contracts,
but retain moral rights.


---------
Copyright
---------

© 2001-2019 FluidAttacks by Fluidsignal Group

-------
License
-------

TBA
EOF

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
