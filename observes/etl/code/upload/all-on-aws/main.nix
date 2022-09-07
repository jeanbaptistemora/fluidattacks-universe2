# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  outputs,
  makeScript,
  ...
}: let
  uploadGroup = outputs."/computeOnAwsBatch/observesCodeEtlUpload";
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
      __argCodeEtlUpload__ = "${uploadGroup}/bin/${uploadGroup.name}";
    };
    name = "observes-etl-code-upload-all-on-aws";
    entrypoint = ./entrypoint.sh;
  }
