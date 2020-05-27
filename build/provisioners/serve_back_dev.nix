let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
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
        (builders.pythonRequirements pkgs).propagatedBuildInputs
      ];

      pyPkgIntegratesBack =
        import ../../django-apps/integrates-back-async pkgs;

      pyPkgReqsApp =
        builders.pythonRequirements ../../deploy/containers/app/requirements.txt;

      pyPkgTracers =
        builders.pythonPackage "tracers==20.5.23574";

      srcDerivationsCerts = import ../derivations/certs pkgs;
    })
  )
