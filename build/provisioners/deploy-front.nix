let
  pkgs = import ../pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (import ../dependencies/requirements.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = []
        ++ (import ../dependencies/version-control.nix pkgs)
        ++ [
          (pkgs.python37.withPackages (ps: with ps; [
            matplotlib
            pip
            python_magic
            selenium
            setuptools
            wheel
          ]))
          pkgs.awscli
          pkgs.curl
          pkgs.cacert
          pkgs.sops
          pkgs.jq
        ];
    })
  )
