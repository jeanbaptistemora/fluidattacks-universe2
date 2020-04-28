let
  pkgs = import ../pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = []
        ++ (import ../dependencies/secret-management.nix pkgs)
        ++ (import ../dependencies/version-control.nix pkgs)
        ++ [
          pkgs.sysctl
          pkgs.nodejs
        ];
    })
  )
