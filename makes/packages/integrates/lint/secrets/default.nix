{ path
, integratesPkgs
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
in
makeDerivation {
  builder = path "/makes/packages/integrates/lint/secrets/builder.sh";
  buildInputs = [
    integratesPkgs.python37Packages.yamllint
    integratesPkgs.yq
  ];
  envConfig = path "/makes/packages/integrates/lint/secrets/config.yaml";
  envYamlSecrets = builtins.map path [
    "/integrates/secrets-development.yaml"
    "/integrates/secrets-production.yaml"
  ];
  name = "integrates-lint-secrets";
}
