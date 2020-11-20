let
  pkgs = import ../pkgs/integrates.nix;
  builders.nodeJsModule = import ../builders/nodejs-module pkgs;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
  builders.rubyGem = import ../builders/ruby-gem pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/dynamodb-local.nix pkgs)
    // (import ../src/minio-local.nix pkgs)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.unzip
        pkgs.awscli
        pkgs.curl
        pkgs.cacert
        pkgs.nodejs
        pkgs.openjdk
        pkgs.p7zip
        pkgs.redis
        pkgs.sops
        pkgs.jq
        pkgs.ruby
        pkgs.iproute
        (pkgs.python37.withPackages (ps: with ps; [
          matplotlib
          pip
          python_magic
          selenium
          setuptools
          wheel
        ]))
        pkgs.libmysqlclient
        pkgs.postgresql
        pkgs.unixODBC
      ];

      nodeJsModuleSecureSpreadsheet =
        builders.nodeJsModule {
          moduleName = "secure-spreadsheet";
          requirement = "secure-spreadsheet@0.1.0";
        };

      pyPkgIntegratesBack =
        import ../../integrates/backend_new/packages/integrates-back pkgs;

      pyPkgReqsApp =
        builders.pythonRequirements ../../integrates/deploy/dependencies/prod-requirements.txt;

      rubyGemAsciiDoctor =
        builders.rubyGem "asciidoctor:2.0.10";

      rubyGemAsciiDoctorPdf =
        builders.rubyGem "asciidoctor-pdf:1.5.0.rc.3";

      rubyGemConcurrentRuby =
        builders.rubyGem "concurrent-ruby:1.1.6";

      srcDerivationsCerts = import ../derivations/certs pkgs;
    })
  )
