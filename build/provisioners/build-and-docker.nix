let
  pkgs = import ../pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = []
        ++ (import ../dependencies/version-control.nix pkgs)
        ++ [
          pkgs.docker
          pkgs.python37Packages.setuptools
          pkgs.zip
          pkgs.python37
          pkgs.awscli
          pkgs.curl
          pkgs.cacert
          pkgs.sops
          pkgs.jq
        ];
    })
  )
