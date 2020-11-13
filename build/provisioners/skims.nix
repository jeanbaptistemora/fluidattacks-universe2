let
  builders.nodeJsModule = import ../builders/nodejs-module pkgs;

  pkgs = import ../pkgs/skims.nix;

  skimsDependencies = import ../src/skims-dependencies.nix pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (import ../src/antlr4.nix pkgs)
    // (skimsDependencies.overriden)
    // (rec {
      name = "builder";

      buildInputs = [
        skimsDependencies.build
        skimsDependencies.runtime
      ];

      nodeJsModuleBugsnagBuildReporter = builders.nodeJsModule {
        moduleName = "bugsnag-build-reporter";
        requirement = "bugsnag-build-reporter@1.0.3";
      };
    })
  )
