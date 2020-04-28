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
        pkgs.nodejs
        pkgs.python37
        pkgs.awscli
        pkgs.curl
        pkgs.cacert
        pkgs.sops
        pkgs.jq
      ];

      pyPkgIntegratesBack =
        builders.pythonPackageLocal ../../django-apps/integrates-back-async;
      pyPkgCasbinInMemoryAdapter =
        builders.pythonPackageLocal ../../django-apps/casbin-in-memory-adapter;
      pyPkgReqs =
        builders.pythonRequirements ./requirements.txt;
      pyPkgReqsApp =
        builders.pythonRequirements ../../deploy/containers/deps-app/requirements.txt;

      pkgGeckoDriver = pkgs.geckodriver;
      pkgFirefox = pkgs.firefox;
    })
  )
