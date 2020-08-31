let
  pkgs = import ../pkgs/skims.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.graphviz
        pkgs.python38
        pkgs.python38Packages.poetry
      ];
    })
  )
