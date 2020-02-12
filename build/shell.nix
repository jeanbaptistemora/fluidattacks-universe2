let
  pkgs = import ./pkgs/stable.nix;

  modules.build.dependencies =  import ./dependencies pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "builder";

    buildInputs = modules.build.dependencies.all;

    pyPkgProspector = modules.build.dependencies.python.prospector;
    pyPkgMandrill = modules.build.dependencies.python.mandrill;

    srcEnv = ./include/env.sh;
    srcIncludeCli = ./include/cli.sh;
    srcIncludeGenericShellOptions = ./include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = ./include/generic/dir-structure.sh;
    srcIncludeHelpers = ./include/helpers.sh;
    srcIncludeJobs = ./include/jobs.sh;
    srcExternalGitlabVariables = pkgs.fetchurl {
      url = "https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/gitlab-variables.sh";
      sha256 = "01sixpmsmm0icngsi66mapxz3149km6iif541fj290saq1zdk4g0";
    };
    srcExternalMail = pkgs.fetchurl {
      url = "https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/mail.py";
      sha256 = "1a7kki53qxdwfh5s6043ygnyzk0liszxn4fygzfkwx7nhsmdf6k3";
    };
    srcExternalSops = pkgs.fetchurl {
      url = "https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh";
      sha256 = "1m2r2yqby9kcwvfsdfzf84ggk4zy408syz26vn9cidvsw8dk00wb";
    };
    srcDotDotToolboxOthers = ../toolbox/others.sh;
  }
