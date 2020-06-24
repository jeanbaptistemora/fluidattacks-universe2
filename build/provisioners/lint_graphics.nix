let
  pkgs = import ../pkgs/stable.nix;

  builders.nodeJsModule = import ../builders/nodejs-module pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.nodejs
      ];

      nodeJsModuleEslint =
        builders.nodeJsModule {
          moduleName = "eslint";
          requirement = "eslint@7.3.1";
        };

      nodeJsModuleEslintConfigStrict =
        builders.nodeJsModule {
          moduleName = "eslint-config-strict";
          requirement = "eslint-config-strict@14.0.1";
        };
    })
  )
