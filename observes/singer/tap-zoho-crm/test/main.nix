# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeDerivation,
  outputs,
  projectPath,
  ...
}:
makeDerivation {
  name = "observes-singer-zoho-crm-test";
  env = {
    envSrc = projectPath inputs.observesIndex.tap.zoho_crm.root;
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.zoho_crm.env.dev}"
    ];
  };
  builder = projectPath "/observes/common/tester/test_builder.sh";
}
