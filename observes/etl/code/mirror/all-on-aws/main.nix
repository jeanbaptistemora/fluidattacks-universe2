# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}: let
  mirrorGroup = outputs."/computeOnAwsBatch/observesCodeEtlMirror";
in
  makeScript {
    searchPaths = {
      source = [
        outputs."/common/utils/git"
        outputs."/common/utils/sops"
        outputs."/observes/common/list-groups"
      ];
    };
    replace = {
      __argCodeEtlMirror__ = "${mirrorGroup}/bin/${mirrorGroup.name}";
    };
    name = "observes-etl-code-mirror-all-on-aws";
    entrypoint = ./entrypoint.sh;
  }
