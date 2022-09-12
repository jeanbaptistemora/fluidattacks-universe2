# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  outputs,
  makeScript,
  makePythonVersion,
  ...
}:
makeScript {
  name = "integrates-execute-machine";
  replace = {
    __argScript__ = ./src/__init__.py;
  };
  searchPaths = {
    bin = [
      (makePythonVersion "3.9")
      outputs."/skims"
      outputs."/melts"
    ];
    source = [
      outputs."/integrates/jobs/execute_machine/env"
      outputs."/common/utils/aws"
      outputs."/common/utils/env"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
