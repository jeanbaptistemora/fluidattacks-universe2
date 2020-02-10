let
  pkgs = import ./pkgs/stable.nix;

  modules = {
    buildPythonPackage = import ./modules/build-python-package pkgs;
    envPython = import ./modules/env/python pkgs;
  };
in
  pkgs.stdenv.mkDerivation rec {
    name = "builder";

    srcEnv = ./include/env.sh;
    srcIncludeGenericShellOptions = ./include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = ./include/generic/dir-structure.sh;
    srcIncludeHelpers = ./include/helpers.sh;
    srcIncludeJobs = ./include/jobs.sh;

    pyPkgProspector = modules.buildPythonPackage "prospector==1.2.0";

    buildInputsModules = with modules; [
      envPython
    ];
    buildInputsPkgs = with pkgs; [
      docker
      hadolint
      nix-linter
      pre-commit
      shellcheck
    ];
    buildInputs = buildInputsModules ++ buildInputsPkgs;
  }
