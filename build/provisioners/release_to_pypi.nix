let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.gnupg
        (pkgs.python37.withPackages (ps: with ps; [
          wheel
          setuptools
        ]))
      ];

      pyPkgTwine = builders.pythonPackage "twine==2.0.0";
    })
  )
