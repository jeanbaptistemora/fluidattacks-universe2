# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makePythonPypiEnvironment,
  makeScript,
  outputs,
  ...
}: let
  name = "integrates-back-test-functional";
  pythonRequirements = makePythonPypiEnvironment {
    inherit name;
    sourcesYaml = ./pypi-sources.yaml;
  };
in
  makeScript {
    inherit name;
    replace = {
      __argIntegratesBackEnv__ = outputs."/integrates/back/env";
    };
    searchPaths = {
      bin = [
        inputs.nixpkgs.tokei
        outputs."/integrates/batch"
        outputs."/integrates/db"
        outputs."/integrates/storage"
      ];
      source = [
        outputs."/common/utils/sops"
        pythonRequirements
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
