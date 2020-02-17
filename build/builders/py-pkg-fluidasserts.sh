# shellcheck shell=bash

source "${stdenv}/setup"
source "${genericShellOptions}"
source "${genericDirs}"

mkdir root/src/repo/conf
mkdir root/src/repo/build
mkdir root/src/repo/build/config

cp -r --no-preserve=mode,ownership \
  "${srcBuildConfigReadmeRst}" root/src/repo/build/config/README.rst
cp -r --no-preserve=mode,ownership \
  "${srcFluidasserts}" root/src/repo/fluidasserts
cp -r --no-preserve=mode,ownership \
  "${srcManifestIn}" root/src/repo/MANIFEST.in
cp -r --no-preserve=mode,ownership \
  "${srcSetupPy}" root/src/repo/setup.py

cp -r --no-preserve=mode,ownership \
  "${fluidassertsDependenciesCache}"/* root/python

cp -r root/src/repo/fluidasserts/ root/python/site-packages/
echo "#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys

from fluidasserts.utils.cli import main

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(main())
" > root/python/site-packages/bin/asserts

mkdir "${out}"
mv root/python/* "${out}"
