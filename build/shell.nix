let
  pkgs = import ./pkgs/stable.nix;

  modules.build.dependencies =  import ./modules/build/dependencies pkgs;
  modules.build.pythonPackage = import ./modules/build/python-package pkgs;
  modules.docker.images.local.nix = import ./modules/docker/images/local/nix pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "builder";

    buildInputs = modules.build.dependencies;

    dockerImagesLocalNix = modules.docker.images.local.nix;

    pyPkgProspector = modules.build.pythonPackage "prospector[with_everything]==1.2.0";

    srcEnv = ./include/env.sh;
    srcIncludeCli = ./include/cli.sh;
    srcIncludeGenericShellOptions = ./include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = ./include/generic/dir-structure.sh;
    srcIncludeHelpers = ./include/helpers.sh;
    srcIncludeJobs = ./include/jobs.sh;
  }
