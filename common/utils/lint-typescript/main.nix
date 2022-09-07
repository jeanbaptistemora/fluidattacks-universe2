# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeTemplate,
  projectPath,
  ...
}:
makeTemplate {
  replace = {
    __argConfig__ = projectPath "/common/utils/lint-typescript";
  };
  name = "utils-bash-lib-lint-typescript";
  template = ./template.sh;
}
