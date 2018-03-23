grep -qr ':status: draft' content

if [ $? -eq 0 ]; then
	echo "Organizing images in draft articles..."
	FILES=$(find output -iname '*.html')

	for DRAFT in $(grep -lr ':status: draft' content); do
		PATTERN=$(echo $DRAFT | sed -e 's/.*-e.\///' -e 's/\/index\.adoc//')
		TARGET_DIR=$(grep -l $PATTERN $FILES | sed 's/index\.html//')
		SRC_DIR=$(grep -l $PATTERN $FILES | sed 's/drafts/blog/; s/index\.html//');
		mv $SRC_DIR* $TARGET_DIR;
	done;
else
	echo "There are no draft articles";
fi
