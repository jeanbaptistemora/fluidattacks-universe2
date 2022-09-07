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
  self = projectPath inputs.observesIndex.tap.mailchimp.root;
in
  makeTemplate {
    name = "observes-singer-tap-mailchimp-env-runtime";
    searchPaths = {
      pythonMypy = [
        self
      ];
      pythonPackage = [
        self
      ];
      source = [
        outputs."${inputs.observesIndex.tap.mailchimp.env.runtime}/python"
        outputs."/observes/common/singer-io/env/runtime"
        outputs."/observes/common/paginator/env/runtime"
        outputs."${inputs.observesIndex.common.utils_logger.env.runtime}"
      ];
    };
  }
