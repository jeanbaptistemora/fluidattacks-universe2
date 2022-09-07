# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeTemplate,
  outputs,
  projectPath,
  ...
}: let
  self = projectPath inputs.observesIndex.common.utils_logger.root;
in
  makeTemplate {
    name = "observes-common-utils-logger-env-runtime";
    searchPaths = {
      pythonPackage = [
        self
      ];
      source = [
        outputs."${inputs.observesIndex.common.utils_logger.env.runtime}/python"
      ];
    };
  }
