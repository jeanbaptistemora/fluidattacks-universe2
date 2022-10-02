# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  __nixpkgs__,
  outputs,
  ...
}: {
  dev = {
    common = {
      bin = [
        __nixpkgs__.alejandra
        outputs."/common/dev/fmt"
      ];
    };
  };
}
