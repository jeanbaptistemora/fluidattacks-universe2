{ forcesPkgs
, makeDerivation
, packages
, path
, ...
}:
let
  makeOci = import (path "/makes/utils/make-oci") path forcesPkgs;
in
makeOci {
  config.WorkingDir = "/src";
  contents = [
    forcesPkgs.bash
    forcesPkgs.coreutils
    packages.forces
    (makeDerivation forcesPkgs {
      builder = path "/makes/packages/forces/oci-build/builder.sh";
      name = "forces-oci-build-customization-layer";
    })
  ];
}
