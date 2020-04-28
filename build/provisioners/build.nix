let
  pkgs = import ../pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = []
        ++ (import ../dependencies/python.nix pkgs)
        ++ (import ../dependencies/secret-management.nix pkgs)
        ++ (import ../dependencies/version-control.nix pkgs)
        ++ [
          pkgs.python37Packages.setuptools
          pkgs.zip
          pkgs.nodejs
        ];
    })
  )
