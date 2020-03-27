let
  pkgs = import ../pkgs/stable.nix;
  pkgs-unstable = import ../pkgs/unstable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = []
        ++ (import ../dependencies/infra.nix pkgs-unstable)
        ++ (import ../dependencies/secret-management.nix pkgs)
        ++ (import ../dependencies/tools.nix pkgs)
        ++ (import ../dependencies/version-control.nix pkgs)
        ++ [
          pkgs.docker
        ];
    })
  )
