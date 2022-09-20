# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.common.postgresClient;
in
  makeTemplate {
    name = "observes-common-postgres-client-env-runtime";
    searchPaths = {
      bin = [
        inputs.nixpkgs.postgresql
      ];
      pythonPackage = [
        self
      ];
      source = [
        (makePythonPypiEnvironment {
          name = "observes-common-postgres-client-env-runtime";
          searchPathsRuntime.bin = [inputs.nixpkgs.gcc inputs.nixpkgs.postgresql];
          searchPathsBuild.bin = [inputs.nixpkgs.gcc inputs.nixpkgs.postgresql];
          sourcesYaml = ./pypi-sources.yaml;
        })
        outputs."/observes/common/purity/env/runtime"
        outputs."${inputs.observesIndex.common.utils_logger.env.runtime}"
      ];
    };
  }
