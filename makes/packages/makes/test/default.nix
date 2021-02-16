{ makesPkgs
, packagesFlattened
, path
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path makesPkgs;
in
makeDerivation {
  builder = path "/makes/packages/makes/test/builder.sh";
  envBuilt = builtins.concatLists [
    (builtins.attrValues (builtins.removeAttrs packagesFlattened [
      # Too much disk
      "integrates.mobile.config.dev-runtime"
      # Needed to avoid infinite recursion
      "makes.test"
    ]))
  ];
  name = "makes-test";
}
