let
  pkgs = import ../pkgs/skims.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (import ../src/antlr4.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.jdk11
        pkgs.git
        pkgs.gradle
        pkgs.graphviz
        pkgs.python38
        pkgs.python38Packages.poetry
      ];
    })
  )
