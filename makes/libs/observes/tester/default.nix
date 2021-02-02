{ nixPkgs
, observesPackage
, path
, testDir
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path nixPkgs;
in
makeDerivation {
  builder = path "/makes/libs/observes/tester/builder.sh";
  buildInputs = [ observesPackage.env ];
  envSrc = observesPackage.packagePath;
  envTestDir = testDir;
  name = "observes-tester";
}
