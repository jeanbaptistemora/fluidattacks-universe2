# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ''
    observes-etl-code-bin "$@"
  '';
  searchPaths = {
    source = [
      outputs."/observes/etl/code/env/bin"
      outputs."/observes/common/import-and-run"
    ];
  };
  name = "observes-etl-code-bin";
}
