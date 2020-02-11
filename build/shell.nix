let
  pkgs = import ./pkgs/stable.nix;

  modules.build.pythonPackage = import ./modules/build/python-package pkgs;
  modules.env.python = import ./modules/env/python pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "builder";

    srcEnv = ./include/env.sh;
    srcIncludeCli = ./include/cli.sh;
    srcIncludeGenericShellOptions = ./include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = ./include/generic/dir-structure.sh;
    srcIncludeHelpers = ./include/helpers.sh;
    srcIncludeJobs = ./include/jobs.sh;

    pyPkgProspector = modules.build.pythonPackage "prospector[with_everything]==1.2.0";

    buildInputs = with pkgs; [
      docker
      git
      hadolint
      nix-linter
      modules.env.python
      shellcheck
      which
    ];
  }
