let
  pkgs = import ../pkgs/stable.nix;

  srcProductGit = pkgs.fetchgit {
    url = "https://gitlab.com/fluidattacks/integrates";
    rev = "036fd066f89951ee1cbfe73a77696b9df015233e";
    sha256 = "0a9x2k900p67pdxd4aarb83lw6w6y3636s7bsk9v7ypph86jk7dn";
  };
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.nix
        pkgs.curl
        pkgs.cacert
      ];

      srcProduct = import srcProductGit;
    })
  )
