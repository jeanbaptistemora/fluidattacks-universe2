let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        (pkgs.python37.withPackages (ps: with ps; [
          matplotlib
          pip
          python_magic
          selenium
          setuptools
          wheel
        ]))
        pkgs.awscli
        pkgs.curl
        pkgs.cacert
        pkgs.sops
        pkgs.jq
        pkgs.git
      ];

      pyPkgIntegratesBack =
        builders.pythonPackageLocal ../../django-apps/integrates-back-async;
      pyPkgCasbinInMemoryAdapter =
        builders.pythonPackageLocal ../../django-apps/casbin-in-memory-adapter;
      pyPkgReqs =
        builders.pythonRequirements ../dependencies/requirements.txt;
      pyPkgReqsApp =
        builders.pythonRequirements ../../deploy/containers/deps-app/requirements.txt;
    })
  )
