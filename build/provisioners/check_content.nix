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
        pkgs.cacert
        pkgs.curl
        pkgs.imagemagick
        pkgs.shellcheck
        (pkgs.python38.withPackages (ps: with ps; [
          termcolor
        ]))
      ];

      pyPkgPreCommit = builders.pythonPackage "pre-commit";
    })
  )
