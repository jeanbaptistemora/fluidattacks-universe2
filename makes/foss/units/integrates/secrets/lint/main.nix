{ projectPath
, makeDerivation
, inputs
, ...
}:
makeDerivation {
  env = {
    envConfig = projectPath "/makes/foss/units/integrates/secrets/lint/config.yaml";
    envYamlSecrets = builtins.map projectPath [
      "/integrates/secrets-development.yaml"
      "/integrates/secrets-production.yaml"
    ];
  };
  builder = projectPath "/makes/foss/units/integrates/secrets/lint/builder.sh";
  name = "integrates-secrets-lint";
  searchPaths.bin = [
    inputs.nixpkgs.python37Packages.yamllint
    inputs.nixpkgs.yq
  ];
}
