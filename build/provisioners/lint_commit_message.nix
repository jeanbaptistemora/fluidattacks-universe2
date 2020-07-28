let
  pkgs = import ../pkgs/stable.nix;
  builders.nodePackage = import ../builders/nodejs-module pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.cacert
        pkgs.curl
        pkgs.nodejs
      ];

      nodeJsModuleCommitlint = builders.nodePackage "@commitlint/cli@9.0.1";
      nodeJsModuleCommitlintConfigConventional =
        builders.nodePackage "@commitlint/config-conventional@9.0.1";
    })
  )
