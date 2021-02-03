{ makesPkgs
, path
, sources
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path makesPkgs;
in
makeDerivation {
  builder = path "/makes/packages/makes/test/builder.sh";
  envBuilt = builtins.concatLists [
    (builtins.attrValues (builtins.removeAttrs sources.apps [
      # Consume a lot of disk
      "integrates/dynamo/oci/deploy"
      "skims/oci-deploy"
    ]))
    (builtins.attrValues (builtins.removeAttrs sources.packages [
      # Needed to avoid infinite recursion
      "makes/test"
      # Consume a lot of disk
      "integrates/dynamo/oci"
      "skims/oci-build"
    ]))
  ];
  name = "makes-test";
}
