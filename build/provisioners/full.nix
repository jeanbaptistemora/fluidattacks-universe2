let
  pkgs = import ../pkgs/stable.nix;

  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
  builders.rubyGem = import ../builders/ruby-gem pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/dynamodb-local.nix pkgs)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.nix-linter
        pkgs.openjdk
        pkgs.redis
        pkgs.shellcheck
        pkgs.nodejs
        pkgs.ruby
        pkgs.kubectl
        pkgs.terraform
        pkgs.tflint
        pkgs.cacert
        pkgs.curl
        pkgs.hostname
        pkgs.jq
        pkgs.rpl
        pkgs.unzip
        pkgs.wget
        pkgs.zip
        pkgs.awscli
        pkgs.sops
        (pkgs.python37.withPackages (ps: with ps; [
          matplotlib
          pip
          python_magic
          selenium
          setuptools
          wheel
        ]))
      ];

      pkgGeckoDriver = pkgs.geckodriver;
      pkgFirefox = pkgs.firefox;

      rubyGemConcurrentRuby =
        builders.rubyGem "concurrent-ruby:1.1.6";

      rubyGemAsciidoctor =
        builders.rubyGem "asciidoctor:2.0.10";

      rubyGemAsciidoctorPdf =
        builders.rubyGem "asciidoctor-pdf:1.5.3";

      pyPkgIntegratesBack =
        builders.pythonPackageLocal ../../django-apps/integrates-back-async;
      pyPkgCasbinInMemoryAdapter =
        builders.pythonPackageLocal ../../django-apps/casbin-in-memory-adapter;
      pyPkgReqs =
        builders.pythonRequirements ../dependencies/requirements.txt;
      pyPkgReqsApp =
        builders.pythonRequirements ../../deploy/containers/app/requirements.txt;

      srcDerivationsCerts = import ../derivations/certs pkgs;
    })
  )
