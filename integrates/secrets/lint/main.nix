# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  projectPath,
  makeDerivation,
  inputs,
  ...
}:
makeDerivation {
  env = {
    envConfig = ./config.yaml;
    envYamlSecrets = builtins.map projectPath [
      "/integrates/secrets/development.yaml"
      "/integrates/secrets/production.yaml"
    ];
  };
  builder = ./builder.sh;
  name = "integrates-secrets-lint";
  searchPaths.bin = [
    inputs.nixpkgs.python39Packages.yamllint
    inputs.nixpkgs.yq
  ];
}
