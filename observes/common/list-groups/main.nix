# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  searchPaths = {
    source = [
      (outputs."${inputs.observesIndex.common.asm_dal.bin}")
    ];
  };
  name = "observes-list-groups";
  template = ./template.sh;
}
