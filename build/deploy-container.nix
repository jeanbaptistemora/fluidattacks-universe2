let
  pkgs = import ./pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation ({}
    // (import ./src/basic.nix pkgs)
    // (import ./src/external.nix pkgs)
    // rec {
      name = "builder";

      buildInputs = import ./dependencies/deploy-container.nix pkgs;
    }
  )
