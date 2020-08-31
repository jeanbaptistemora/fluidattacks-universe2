let
  pkgs = import ../pkgs/integrates.nix;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/c3.nix pkgs)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.unzip
        pkgs.awscli
        pkgs.curl
        pkgs.sops
        pkgs.jq
        pkgs.python37
      ];

      pyPkgIntegratesBack =
        import ../../integrates/django-apps/integrates-back-async pkgs;
      pyPkgReqsApp =
        builders.pythonRequirements ../../integrates/deploy/containers/app/requirements.txt;
    })
  )
