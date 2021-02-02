{ nixPkgs, path }:
let
  localLib = import (path "/makes/libs/observes/packages") {
    inherit nixPkgs path;
  };
  tester = import (path "/makes/libs/observes/tester");
  test = observesPackage: tester {
    inherit nixPkgs observesPackage path;
    testDir = "tests";
  };
in
builtins.mapAttrs (k: _: test localLib.${k}) localLib
