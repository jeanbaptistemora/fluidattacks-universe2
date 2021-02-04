{ nixPkgs, path }:
let
  packageConfig = import (path "/makes/libs/observes/packages/config") {
    inherit nixPkgs path;
  };
  packageBuilder = import (path "/makes/libs/observes/build-package");
  mkDerivation = { packageName, projectDir, pythonReqs, buildInputsList ? [ ] }: rec {
    name = packageName;
    packagePath = projectDir;
    env = packageBuilder {
      name = packageName;
      buildInputs = buildInputsList;
      inherit nixPkgs;
      inherit packageName;
      inherit path;
      inherit projectDir;
      python = nixPkgs.python38;
      inherit pythonReqs;
    };
    buildInputs = [ env ] ++ buildInputsList;
  };
  getLocalReqs = pkgName: self: builtins.map (pkg: self.${pkg}.env) packageConfig.${pkgName}.local;
  getPackageConfig = packageName: self: {
    inherit packageName;
    projectDir = packageConfig.${packageName}.srcPath;
    pythonReqs = packageConfig.${packageName}.python;
    buildInputsList = packageConfig.${packageName}.nix ++ getLocalReqs packageName self;
  };
  lib = rec {
    self = builtins.mapAttrs
      (
        pkgName: _: mkDerivation (getPackageConfig pkgName self)
      )
      packageConfig;
  };
in
lib.self
