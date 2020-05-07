let
  pkgs = import ../pkgs/stable.nix;

  builders.turtleShell = import ../builders/turtle-shell pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.awscli
        pkgs.git
        pkgs.jq
        pkgs.nodejs
        pkgs.openjdk
        pkgs.sops
      ];

      turtleShell = builders.turtleShell "37.0.0";
    })
  )
