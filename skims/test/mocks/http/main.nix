# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "skims-test-mocks-http";
  replace = {
    __argApp__ = ./src;
  };
  entrypoint = ./entrypoint.sh;
  searchPaths.source = [outputs."/skims/test/mocks/http/env"];
}
