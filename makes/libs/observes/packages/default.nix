{ nixPkgs, path }:
let
  rawPackageConfig = import (path "/makes/libs/observes/packages/config") {
    inherit nixPkgs path;
  };
  packageBuilder = import (path "/makes/libs/observes/build-package");
  mkPackage = packageConfig: packageBuilder {
    inherit nixPkgs packageConfig path;
  };
  getLocalReqs = pkgName: self:
    builtins.map (pkg: self.${pkg}) rawPackageConfig.${pkgName}.local;
  getPackageConfig = packageName: self: {
    inherit packageName;
    srcPath = rawPackageConfig.${packageName}.srcPath;
    reqs = rawPackageConfig.${packageName} // {
      local = getLocalReqs packageName self;
    };
    buildInputs = rawPackageConfig.${packageName}.nix;
    python = nixPkgs.python38;
  };
  lib = rec {
    self = builtins.mapAttrs
      (
        pkgName: _: mkPackage (getPackageConfig pkgName self)
      )
      rawPackageConfig;
  };
in
lib.self
