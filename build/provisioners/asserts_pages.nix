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
        pkgs.perl
        pkgs.cacert
        pkgs.python37
        pkgs.python37Packages.selenium
        pkgs.python37Packages.brotli
      ];

      pyPkgAsserts = import ../../asserts pkgs;

      pyPkgGitfame = builders.pythonPackage "git-fame==1.10.1";
      pyPkgSphinx = builders.pythonPackage "sphinx==2.2.1";
      pyPkgSphinxrtdtheme = builders.pythonPackage "sphinx-rtd-theme==0.4.3";
      pyPkgSphinxautodoctypehints = builders.pythonPackage "sphinx-autodoc-typehints==1.10.3";
    })
  )
