let
  pkgs = import ../pkgs/stable.nix;

  builders.nodeJsModule = import ../builders/nodejs-module pkgs;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.awscli
        pkgs.cacert
        pkgs.curl
        pkgs.git
        pkgs.jq
        pkgs.zip
      ];
    })
  )
