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
        pkgs.curl
        pkgs.cacert
        pkgs.python37
      ];

      pyPkgMandrill = builders.pythonPackage "mandrill-37==1.1.0";
      pyPkgGitPython = builders.pythonPackage "GitPython==3.1.0";
    })
  )
