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
        pkgs.glibcLocales
        pkgs.shellcheck
        pkgs.html-tidy
        (pkgs.python38.withPackages (ps: with ps; [
          pylint
          flake8
        ]))
      ];

      pyPkgPreCommit = builders.pythonPackage "pre-commit==2.2.0";
    })
  )
