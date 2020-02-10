let
  pkgs = import ./pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation rec {
    name = "builder";

    srcGenericShellOptions = ./include/generic/shell-options.sh;
    srcGenericDirStructure = ./include/generic/dir-structure.sh;
    srcHelpers = ./include/helpers.sh;

    buildInputs = with pkgs; [
      docker
      hadolint
      nix-linter
      shellcheck
    ];
  }
