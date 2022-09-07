# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/etl/gitlab"
    ];
    source = [
      outputs."/observes/common/db-creds"
      outputs."/common/utils/aws"
    ];
  };
  name = "observes-etl-gitlab-challenges";
  entrypoint = ./entrypoint.sh;
}
