let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
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
        import ../../django-apps/integrates-back-async pkgs;
      pyPkgCasbinInMemoryAdapter =
        builders.pythonPackageLocal ../../django-apps/casbin-in-memory-adapter;

      pyPkgReqs =
        builders.pythonRequirements ../dependencies/requirements.txt;
      pyPkgReqsApp =
        builders.pythonRequirements ../../deploy/containers/app/requirements.txt;
    })
  )
