let
  pkgs = import ./pkgs/stable.nix;

  modules.build.dependencies =  import ./modules/build/dependencies pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "builder";

    buildInputs = modules.build.dependencies.all;

    pyPkgProspector = modules.build.dependencies.python.prospector;

    srcEnv = ./include/env.sh;
    srcIncludeCli = ./include/cli.sh;
    srcIncludeGenericShellOptions = ./include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = ./include/generic/dir-structure.sh;
    srcIncludeHelpers = ./include/helpers.sh;
    srcIncludeJobs = ./include/jobs.sh;
  }
