let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (import ../src/dynamodb-local.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.awscli
        pkgs.curl
        pkgs.sops
        pkgs.jq
        pkgs.redis
        pkgs.openjdk
        pkgs.unzip
        pkgs.cacert
        pkgs.python37
      ];

      pyPkgIntegratesBack =
        import ../../integrates/django-apps/integrates-back-async pkgs;

      pyPkgReqs =
        builders.pythonRequirements ../dependencies/requirements.txt;
      pyPkgReqsApp =
        builders.pythonRequirements ../../integrates/deploy/containers/app/requirements.txt;
    })
  )
