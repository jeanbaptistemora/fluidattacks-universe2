{ nixPkgs, path }:
let
  observesPackages = import (path "/makes/libs/observes/packages") {
    inherit nixPkgs path;
  };

  mkBin = config: import (path "/makes/libs/observes/build-bin") {
    inherit nixPkgs path;
    entrypoint = config.entrypoint;
    name = config.binName;
    packageEnv = config.package.template;
    python = nixPkgs.python38;
  };
in
builtins.mapAttrs
  (_: mkBin)
  (import (path "/makes/libs/observes/bins/config") observesPackages)
