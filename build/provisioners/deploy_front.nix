let
  pkgs = import ../pkgs/stable.nix;
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
        import ../../django-apps/integrates-back-async pkgs;
      pyPkgReqsApp =
        builders.pythonRequirements ../../deploy/containers/app/requirements.txt;
    })
  )
