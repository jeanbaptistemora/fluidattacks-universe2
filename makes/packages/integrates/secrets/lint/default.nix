{ path
, makeDerivation
, nixpkgs
, ...
}:
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
      nixpkgs.python37Packages.yamllint
      nixpkgs.yq
    ];
  };
}
