let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.awscli
        pkgs.curl
        pkgs.sops
        pkgs.jq
        pkgs.python37
      ];

      pkgGeckoDriver = pkgs.geckodriver;
      pkgFirefox = pkgs.firefox;

      pyPkgIntegratesBack =
        import ../../django-apps/integrates-back-async pkgs;

      pyPkgReqs =
        builders.pythonRequirements ../dependencies/requirements.txt;
      pyPkgReqsApp =
        builders.pythonRequirements ../../deploy/containers/app/requirements.txt;
    })
  )
