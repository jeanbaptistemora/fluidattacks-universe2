let
  builders.nodeJsModule = import ../builders/nodejs-module pkgs;

  pkgs = import ../pkgs/skims.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (import ../src/antlr4.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.awscli
        pkgs.jdk11
        pkgs.git
        pkgs.gnutar
        pkgs.gradle
        pkgs.graphviz
        pkgs.nodejs
        pkgs.python38
        pkgs.python38Packages.poetry
      ];

      nodeJsModuleBugsnagBuildReporter = builders.nodeJsModule {
        moduleName = "bugsnag-build-reporter";
        requirement = "bugsnag-build-reporter@1.0.3";
      };
    })
  )
