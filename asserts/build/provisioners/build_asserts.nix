let
  pkgs = import ../pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
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
