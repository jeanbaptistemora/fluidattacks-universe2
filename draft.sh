#!/usr/bin/env bash

# This script enables the use of articles with draft status, so unfinished
# articles can be reviewed by peers but not displayed in production.

# Check if there are articles with draft status
if grep -qr ':status: draft' content; then

  echo "Organizing images in draft articles..."
  FILES="$(find output -iname '*.html')"

  # Get the filenames of every article with draft status
  grep -lr ':status: draft' content | while IFS= read -r DRAFT; do

    # Extract the slug of the articles
    PATTERN=$(echo "$DRAFT" | sed -e 's/.*-e.\///' -e 's/\/index\.adoc//')

    # Locate the folder of the generated HTML of the article draft
    TARGET_DIR=$(grep -l "$PATTERN" "$FILES" | sed 's/index\.html//')

    # Locate the folder where the images of the article draft were saved
    SRC_DIR=$(grep -l "$PATTERN" "$FILES" | sed 's/drafts/blog/; s/index\.html//');

    # Move the images to the folder of the generated HTML of the draft article
    mv "$SRC_DIR*" "$TARGET_DIR";
  done;
else
  echo "There are no draft articles";
fi
