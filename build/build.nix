let
  pkgs = import ./pkgs/stable.nix;

  builders.pythonPackage = import ./builders/python-package pkgs;

in
  pkgs.stdenv.mkDerivation ({}
    // (import ./src/basic.nix pkgs)
    // (import ./src/external.nix pkgs)
    // rec {
      name = "builder";

      buildInputs = []
        ++ (import ./dependencies/interpreters.nix pkgs)
        ++ (import ./dependencies/secret-management.nix pkgs)
        ++ (import ./dependencies/version-control.nix pkgs)
        ++ [
          pkgs.python37Packages.setuptools
          pkgs.zip
        ];
    }
  )
