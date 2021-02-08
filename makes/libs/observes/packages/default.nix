{ nixPkgs, path }:
let
  rawPackageConfig = import (path "/makes/libs/observes/packages/config") {
    inherit nixPkgs path;
  };
  packageBuilder = import (path "/makes/libs/observes/build-package");
  mkDerivation = packageConfig: rec {
    name = packageConfig.packageName;
    packagePath = packageConfig.srcPath;
    env = packageBuilder {
      inherit nixPkgs;
      inherit packageConfig;
      inherit path;
    };
    buildInputs = [ env ] ++ packageConfig.buildInputsList;
  };
  getLocalReqs = pkgName: self: builtins.map (pkg: self.${pkg}.env) rawPackageConfig.${pkgName}.local;
  getPackageConfig = packageName: self: {
    inherit packageName;
    srcPath = rawPackageConfig.${packageName}.srcPath;
    reqs = rawPackageConfig.${packageName};
    buildInputsList = rawPackageConfig.${packageName}.nix ++ getLocalReqs packageName self;
    python = nixPkgs.python38;
  };
  lib = rec {
    self = builtins.mapAttrs
      (
        pkgName: _: mkDerivation (getPackageConfig pkgName self)
      )
      rawPackageConfig;
  };
in
lib.self
