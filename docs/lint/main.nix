# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "docs-lint";
  searchPaths = {
    source = [
      outputs."/common/utils/lint-npm-deps"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
