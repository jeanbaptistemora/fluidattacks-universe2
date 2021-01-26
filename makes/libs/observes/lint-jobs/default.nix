{ nixPkgs, path }:
let
  localLib = import (path "/makes/libs/observes/packages") {
    inherit nixPkgs path;
  };
  linter = import (path "/makes/libs/observes/linter");
  lint = packageLib: linter {
    inherit nixPkgs path;
    packageSrcPath = packageLib.packagePath;
    buildInputs = packageLib.buildInputs;
  };
in
builtins.mapAttrs (k: _: lint localLib.${k}) localLib
