# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "integrates-front-lint";
  searchPaths.bin = [
    outputs."/integrates/front/lint/eslint"
    outputs."/integrates/front/lint/stylelint"
  ];
  entrypoint = ./entrypoint.sh;
}
