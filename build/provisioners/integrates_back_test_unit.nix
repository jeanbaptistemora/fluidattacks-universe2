let
  pkgs = import ../pkgs/integrates.nix;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/minio-local.nix pkgs)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.awscli
        pkgs.curl
        pkgs.sops
        pkgs.jq
        pkgs.openjdk
        pkgs.unzip
        pkgs.cacert
        pkgs.python37
        (import ../..).integrates-dynamo
        (import ../..).integrates-redis
      ];

      pyPkgIntegratesBack =
        import ../../integrates/back/packages/integrates-back pkgs;

      pyPkgReqs =
        builders.pythonRequirements ../../integrates/deploy/dependencies/dev-requirements.txt;
      pyPkgReqsApp =
        builders.pythonRequirements ../../integrates/deploy/dependencies/prod-requirements.txt;
    })
  )
