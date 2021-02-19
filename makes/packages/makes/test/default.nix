{ makesPkgs
, packagesFlattened
, path
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path makesPkgs;
in
makeDerivation {
  arguments = {
    envBuilt = builtins.concatLists [
      (builtins.attrValues (builtins.removeAttrs packagesFlattened [
        # Too much disk
        "integrates.mobile.config.dev-runtime"
        # Needed to avoid infinite recursion
        "makes.test"
      ]))
    ];
  };
  builder = path "/makes/packages/makes/test/builder.sh";
  name = "makes-test";
}
