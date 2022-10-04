# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeScript,
  outputs,
  ...
}: let
  dynamodb = outputs."/integrates/db/dynamodb";
  opensearch = outputs."/integrates/db/opensearch";
  streams = outputs."/integrates/streams";
in
  makeScript {
    name = "integrates-db";
    searchPaths = {
      bin = [
        dynamodb
        opensearch
        streams
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
