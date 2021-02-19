{ nixPkgs
, observesPackage
, path
, testDir
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path nixPkgs;
in
makeDerivation {
  arguments = {
    envSrc = observesPackage.packagePath;
    envTestDir = testDir;
  };
  builder = path "/makes/libs/observes/tester/builder.sh";
  name = "observes-tester-${observesPackage.name}";
  searchPaths = {
    envSources = [ observesPackage.template ];
  };
}
