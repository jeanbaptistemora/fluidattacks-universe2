# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  name = "melts-lib";
  searchPaths = {
    bin = [outputs."/melts"];
    source = [outputs."/common/utils/git"];
  };
  template = ./template.sh;
}
