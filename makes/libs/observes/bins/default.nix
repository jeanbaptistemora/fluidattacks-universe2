{ nixPkgs, path }:
let
  nixpkgs2 = import (path "/makes/libs/observes/packages") {
    inherit nixPkgs path;
  };
  binConfig = import (path "/makes/libs/observes/bins/config") {
    inherit nixpkgs2;
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
