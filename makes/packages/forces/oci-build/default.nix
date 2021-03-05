{ nixpkgs
, makeDerivation
, packages
, path
, ...
}:
let
  makeOci = import (path "/makes/utils/make-oci") path nixpkgs;
in
makeOci {
  config.WorkingDir = "/src";
  contents = [
    nixpkgs.bash
    nixpkgs.coreutils
    packages.forces
    (makeDerivation {
      builder = path "/makes/packages/forces/oci-build/builder.sh";
      name = "forces-oci-build-customization-layer";
    })
  ];
}
