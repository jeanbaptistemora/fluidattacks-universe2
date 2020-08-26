let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.awscli
        pkgs.sops
        pkgs.jq
        (pkgs.python37.withPackages (ps: with ps; [
          wheel
          setuptools
        ]))
      ];

      pyPkgTwine = builders.pythonPackage "twine==2.0.0";
    })
  )
