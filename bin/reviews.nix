let
  pkgs = import ../build/pkgs/stable.nix;

  builders.pythonPackageLocal = import ../build/builders/python-package-local pkgs;
  builders.nodeJsModule = import ../build/builders/nodejs-module pkgs;
in
  pkgs.stdenv.mkDerivation rec {
    name = "bin";

    buildInputs = [
      pkgs.nodejs
    ];

    nodeJsModuleCommitlint =
      builders.nodeJsModule {
        moduleName = "commitlint";
        requirement = "@commitlint/cli@9.0.1";
      };

    nodeJsModuleCommitlintConfigConventional =
      builders.nodeJsModule {
        moduleName = "commitlint-config-conventional";
        requirement = "@commitlint/config-conventional@9.0.1";
      };

    pyPkgReviews = builders.pythonPackageLocal { path = ../reviews; };
  }
