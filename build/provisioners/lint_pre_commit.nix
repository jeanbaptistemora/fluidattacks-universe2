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
        pkgs.shellcheck
        (pkgs.python38.withPackages (ps: with ps; [
          pylint
          flake8
        ]))
      ];

      pyPkgPreCommit = builders.pythonPackage "pre-commit==2.2.0";
    })
  )
