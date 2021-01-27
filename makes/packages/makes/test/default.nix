{ makesPkgs
, path
, sources
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path makesPkgs;
in
makeDerivation {
  builder = "success";
  envBuilt = builtins.concatLists [
    (builtins.attrValues (builtins.removeAttrs sources.apps [
      "skims/oci-deploy" # Consumes a lot of disk
    ]))
    (builtins.attrValues (builtins.removeAttrs sources.packages [
      "makes/test" # Needed to avoid infinite recursion
      "skims/oci-build" # Consumes a lot of disk
    ]))
  ];
  name = "makes-test";
}
