let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.unzip
        pkgs.awscli
        pkgs.curl
        pkgs.cacert
        pkgs.sops
        pkgs.jq
      ];

      pyPkgIntegratesBack =
        import ../../django-apps/integrates-back-async pkgs;
      pyPkgCasbinInMemoryAdapter =
        builders.pythonPackageLocal ../../django-apps/casbin-in-memory-adapter;

      pyPkgReqsApp =
        builders.pythonRequirements ../../deploy/containers/app/requirements.txt;

      srcDerivationsCerts = import ../derivations/certs pkgs;
    })
  )
