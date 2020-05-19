let
  pkgs = import ../pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        (pkgs.python37.withPackages (ps: with ps; [
          wheel
          setuptools
        ]))
      ];
    })
  )
