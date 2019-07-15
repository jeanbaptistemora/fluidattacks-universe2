#!/usr/bin/env bash

# This file checks if mobile/package.json OR
# mobile/Gemfile OR deploy/containers/mobile/Dockerfile
# were modified. If any of the files was modified,
# It runs a kaniko-build for mobile.

# Get modified files base on whether branch is master or dev
if [[ "$CI_COMMIT_REF_NAME" == 'master' ]]; then
  CHANGED=$(git diff --name-only "$CI_COMMIT_BEFORE_SHA" "$CI_COMMIT_SHA")
else
  CHANGED=$(git diff --name-only origin/master HEAD)
fi

# Keep only existing files in changed
for FILE in $CHANGED; do
  if [ -f "$FILE" ]; then
    NEW_CHANGED+="$FILE "
  fi
done
CHANGED=$NEW_CHANGED

echo 'Files modified in this branch:'
echo "$CHANGED"

FILES=(
  'mobile/package.json'
  'mobile/Gemfile'
  'deploy/containers/mobile/Dockerfile'
)

for CHANGED_FILE in $CHANGED; do
  for FILE in "${FILES[@]}"; do
    if [[ "$CHANGED_FILE" == "$FILE" ]]; then
      echo "$FILE was modified. Running mobile builder."
      ./ci-scripts/kaniko-build.sh mobile
      exit $?
    fi
  done
done
echo 'No relevant files for mobile build were modified. Skipping build.'