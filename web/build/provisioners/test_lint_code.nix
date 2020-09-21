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
        pkgs.nodejs
        pkgs.python38
      ];

      pyPkgPreCommit = builders.pythonPackage "pre-commit==2.2.0";
      pyPkgPyLint = builders.pythonPackage "pylint==2.4.4";
      pyPkgFlake8 = builders.pythonPackage "flake8==3.7.9";
    })
  )
