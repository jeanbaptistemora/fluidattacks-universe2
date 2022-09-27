# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# This is a temporary job, used to unify all integrates' buckets into one
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "integrates-move-s3";
  searchPaths = {
    source = [
      outputs."/common/utils/aws"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
