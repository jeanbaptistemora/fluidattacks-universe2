{ path
, nixpkgs2
, ...
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path nixpkgs2;
in
makeDerivation {
  arguments = {
    envConfig = path "/makes/packages/integrates/secrets/lint/config.yaml";
    envYamlSecrets = builtins.map path [
      "/integrates/secrets-development.yaml"
      "/integrates/secrets-production.yaml"
    ];
  };
  builder = path "/makes/packages/integrates/secrets/lint/builder.sh";
  name = "integrates-secrets-lint";
  searchPaths = {
    envPaths = [
      nixpkgs2.python37Packages.yamllint
      nixpkgs2.yq
    ];
  };
}
