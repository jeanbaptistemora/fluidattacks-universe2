{ nixPkgs, path }:
let
  observesPkgs = import (path "/makes/libs/observes/packages") {
    inherit nixPkgs path;
  };
  binConfig = import (path "/makes/libs/observes/bins/config") {
    inherit observesPkgs;
  };
  binBuilder = import (path "/makes/libs/observes/build-bin");
  mkBin = config: binBuilder {
    inherit nixPkgs path;
    entrypoint = config.entrypoint;
    name = config.binName;
    packageEnv = config.package.template;
    python = nixPkgs.python38;
  };
in
builtins.mapAttrs (_: mkBin) binConfig
