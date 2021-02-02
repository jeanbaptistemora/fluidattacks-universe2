{ nixPkgs, path }:
let
  localLib = import (path "/makes/libs/observes/packages") {
    inherit nixPkgs path;
  };
  linter = import (path "/makes/libs/observes/linter");
  lint = observesPackage: linter {
    inherit nixPkgs observesPackage path;
  };
in
builtins.mapAttrs (k: _: lint localLib.${k}) localLib
