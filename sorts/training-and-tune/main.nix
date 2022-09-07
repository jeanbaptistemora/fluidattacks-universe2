# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "sorts-training-and-tune";
  searchPaths = {
    bin = [
      outputs."/sorts/training"
      outputs."/sorts/tune"
    ];
  };
  entrypoint = ''
    : \
      && sorts-training \
      && sorts-tune
  '';
}
