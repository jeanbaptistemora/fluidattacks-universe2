let
  pkgs = import ../pkgs/stable.nix;

  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/dynamodb-local.nix pkgs)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.openjdk
        pkgs.redis
        pkgs.unzip
        pkgs.nodejs
        pkgs.awscli
        pkgs.curl
        pkgs.cacert
        pkgs.sops
        pkgs.jq
        (pkgs.python37.withPackages (ps: with ps; [
          matplotlib
          pip
          python_magic
          selenium
          setuptools
          wheel
        ]))
      ];

      pyPkgIntegratesBack =
        builders.pythonPackageLocal ../../django-apps/integrates-back-async;
      pyPkgCasbinInMemoryAdapter =
        builders.pythonPackageLocal ../../django-apps/casbin-in-memory-adapter;
      pyPkgReqs =
        builders.pythonRequirements ../dependencies/requirements.txt;
      pyPkgReqsApp =
        builders.pythonRequirements ../../deploy/containers/app/requirements.txt;
    })
  )
