let
  pkgs = import ../pkgs/stable.nix;

  builders.nodejsModule = import ../builders/nodejs-module pkgs;
  builders.pythonPackage = import ../builders/python-package pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
  builders.rubyGem = import ../builders/ruby-gem pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../dependencies/requirements.nix pkgs)
    // (import ../dependencies/requirements-async.nix pkgs)
    // (import ../dependencies/selenium.nix pkgs)
    // (import ../src/basic.nix)
    // (import ../src/dynamodb-local.nix pkgs)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = []
        ++ (import ../dependencies/infra.nix pkgs)
        ++ (import ../dependencies/nodejs.nix pkgs)
        ++ (import ../dependencies/python.nix pkgs)
        ++ (import ../dependencies/python-with-tools.nix pkgs)
        ++ (import ../dependencies/ruby.nix pkgs)
        ++ (import ../dependencies/secret-management.nix pkgs)
        ++ (import ../dependencies/tools.nix pkgs)
        ++ (import ../dependencies/version-control.nix pkgs)
        ++ [
          pkgs.nix-linter
          pkgs.openjdk
          pkgs.redis
          pkgs.shellcheck
        ];

      nodejsModuleGraphqlSchemaLinter =
        builders.nodejsModule "graphql-schema-linter@0.2.4";

      rubyGemConcurrentRuby =
        builders.rubyGem "concurrent-ruby:1.1.6";

      rubyGemAsciidoctor =
        builders.rubyGem "asciidoctor:2.0.10";

      rubyGemAsciidoctorPdf =
        builders.rubyGem "asciidoctor-pdf:1.5.3";

      srcDerivationsCerts = import ../derivations/certs pkgs;
    })
  )
