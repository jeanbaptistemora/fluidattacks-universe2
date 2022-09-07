# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  outputs,
  makeScript,
  ...
}: let
  migrate = outputs."/computeOnAwsBatch/observesCodeEtlMigration2";
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
      __argMigrate__ = "${migrate}/bin/${migrate.name}";
    };
    name = "observes-etl-code-upload-migration-fa-hash-range-on-aws";
    entrypoint = ./entrypoint.sh;
  }
