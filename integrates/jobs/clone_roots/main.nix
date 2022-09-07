# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  makePythonVersion,
  outputs,
  ...
}:
makeScript {
  name = "integrates-jobs-clone-roots";
  replace = {
    __argPythonEnv__ = outputs."/integrates/jobs/clone_roots/env";
    __argScript__ = ./src/__init__.py;
  };
  searchPaths = {
    bin = [(makePythonVersion "3.9")];
    source = [
      outputs."/common/utils/aws"
      outputs."/common/utils/env"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
