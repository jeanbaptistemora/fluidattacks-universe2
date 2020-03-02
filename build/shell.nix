let
  pkgs = import ./pkgs/stable.nix;
  builders.nodejsModule = import ./builders/nodejs-module pkgs;
  builders.pythonPackage = import ./builders/python-package pkgs;
  builders.pythonPackageLocal = import ./builders/python-package-local pkgs;
  builders.pythonRequirements = import ./builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "builder";

    buildInputs = import ./dependencies pkgs;

    nodejsModuleGraphqlSchemaLinter =
      builders.nodejsModule "graphql-schema-linter@0.2.4";
    pyPkgIntegratesBack =
      builders.pythonPackageLocal ../django-apps/integrates-back;
    pyPkgReqsDevelopment =
      builders.pythonRequirements ../deploy/containers/deps-development/requirements.txt;
    pyPkgReqsProduction =
      builders.pythonRequirements ../deploy/containers/deps-production/requirements.txt;
    pyPkgUvicorn =
      builders.pythonPackage "uvicorn==0.11.3";

    srcCiScriptsHelpersOthers = ../ci-scripts/helpers/others.sh;
    srcCiScriptsHelpersSops = ../ci-scripts/helpers/sops.sh;
    srcEnv = ./include/env.sh;
    srcIncludeCli = ./include/cli.sh;
    srcIncludeGenericShellOptions = ./include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = ./include/generic/dir-structure.sh;
    srcIncludeHelpers = ./include/helpers.sh;
    srcIncludeJobs = ./include/jobs.sh;
    srcExternalGitlabVariables = pkgs.fetchurl {
      url = "https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/gitlab-variables.sh";
      sha256 = "13y7xd9n0859lgncljxbkgvdhx9akxflkarcv4klsn9cqz3mgr06";
    };
    srcExternalMail = pkgs.fetchurl {
      url = "https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/mail.py";
      sha256 = "1a7kki53qxdwfh5s6043ygnyzk0liszxn4fygzfkwx7nhsmdf6k3";
    };
    srcExternalSops = pkgs.fetchurl {
      url = "https://gitlab.com/fluidattacks/public/raw/master/shared-scripts/sops.sh";
      sha256 = "1m2r2yqby9kcwvfsdfzf84ggk4zy408syz26vn9cidvsw8dk00wb";
    };
    srcExternalDynamoDbLocal = pkgs.fetchurl {
      url = "https://s3-us-west-2.amazonaws.com/dynamodb-local/dynamodb_local_latest.zip";
      sha256 = "0crca9j5mizxl3iqbgmfs1vj7hxpxzqgnd75jc3c7v836ydl86zm";
    };
    srcDerivationsCerts = import ./derivations/certs pkgs;
  }
