let
  pkgs = import ../pkgs/stable.nix;

  srcProductGit = pkgs.fetchgit {
    url = "https://gitlab.com/fluidattacks/integrates";
    rev = "edd2d818d137c2a7cadfc1b02af0d7ad1e68c3b0";
    sha256 = "1xrxjky4wcw8gax453ml8m5wdwr277ivmhzn476i4v0rbj8d7h5c";
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
