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
        (builders.pythonPackage {}).propagatedBuildInputs
      ];

      pyPkgBugsnag = builders.pythonPackage {requirement ="bugsnag==3.6.1";};

    })
  )
