# shellcheck shell=bash

export PATH="${out}/bin/:${PATH}"
python3 -m pip  install . --prefix=$out
cp -r ${pyPkgFluidattacks}/site-packages/* ${out}/bin | true
