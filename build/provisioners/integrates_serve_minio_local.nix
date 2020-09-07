let
  pkgs = import ../pkgs/integrates.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/minio-local.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.awscli
        pkgs.sops
        pkgs.jq
        (builders.pythonPackage {}).propagatedBuildInputs
        (builders.pythonRequirements pkgs).propagatedBuildInputs
      ];

      pyPkgIntegratesBack =
        import ../../integrates/django-apps/integrates-back-async pkgs;

      pyPkgReqsApp =
        builders.pythonRequirements ../../integrates/deploy/containers/app/requirements.txt;

    })
  )
