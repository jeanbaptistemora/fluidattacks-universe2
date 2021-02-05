{ makesPkgs
, packages
, path
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path makesPkgs;
in
makeDerivation {
  builder = path "/makes/packages/makes/test/builder.sh";
  envBuilt = builtins.concatLists [
    (builtins.attrValues (builtins.removeAttrs packages [
      # Too much disk
      "integrates/mobile/config/development"
      # Needed to avoid infinite recursion
      "makes/test"
    ]))
  ];
  name = "makes-test";
}
