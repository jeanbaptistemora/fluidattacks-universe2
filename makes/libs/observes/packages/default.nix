{ nixPkgs, path }:
let
  packageConfig = import (path "/makes/libs/observes/packages/config") {
    inherit nixPkgs path;
  };
  packageBuilder = import (path "/makes/libs/observes/build-package");
  mkDerivation = { packageName, projectDir, pythonReqs, buildInputsList ? [ ] }: rec {
    packagePath = projectDir;
    env = packageBuilder {
      inherit nixPkgs packageName path projectDir pythonReqs;
      python = nixPkgs.python38;
      buildInputs = buildInputsList;
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
