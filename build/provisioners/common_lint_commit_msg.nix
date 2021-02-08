let
  pkgs = import ../pkgs/common.nix;
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

      nodeJsModuleCommitlint =
        builders.nodeJsModule {
          moduleName = "commitlint";
          requirement = "@commitlint/cli@11.0.0";
        };
      nodeJsModuleCommitlintConfigConventional =
        builders.nodeJsModule {
          moduleName = "commitlint-config-conventional";
          requirement = "@commitlint/config-conventional@11.0.0";
        };
    })
  )
