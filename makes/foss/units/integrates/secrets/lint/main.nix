{ projectPath
, makeDerivation
, inputs
, ...
}:
makeDerivation {
  env = {
    envConfig = ./config.yaml;
    envYamlSecrets = builtins.map projectPath [
      "/integrates/secrets-development.yaml"
      "/integrates/secrets-production.yaml"
    ];
  };
  builder = ./builder.sh;
  name = "integrates-secrets-lint";
  searchPaths.bin = [
    inputs.nixpkgs.python39Packages.yamllint
    inputs.nixpkgs.yq
  ];
}
