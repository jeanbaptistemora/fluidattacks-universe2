# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeDerivationParallel,
  outputs,
  ...
}:
makeDerivationParallel {
  dependencies = [
    outputs."/integrates/front/lint/eslint"
    outputs."/integrates/front/lint/stylelint"
  ];
  name = "integrates-front-lint";
}
