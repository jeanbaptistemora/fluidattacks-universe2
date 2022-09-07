# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makePythonPypiEnvironment,
  makeScript,
  projectPath,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argSecretsDev__ = projectPath "/integrates/secrets/development.yaml";
  };
  name = "integrates-coverage";
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.git
      outputs."/common/utils/codecov"
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "integrates-coverage";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/common/utils/aws"
      outputs."/common/utils/sops"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
