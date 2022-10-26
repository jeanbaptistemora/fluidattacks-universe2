# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  projectPath,
  makeDynamoDb,
  makeScript,
  ...
}: let
  dynamodb_data = makeScript {
    replace = {
      __argDbData__ = projectPath "/integrates/back/test/data";
      __argNewDbDesign__ = projectPath "/integrates/arch/database-design.json";
    };
    name = "data-for-db";
    searchPaths = {
      bin = [
        inputs.nixpkgs.awscli
        inputs.nixpkgs.git
        inputs.nixpkgs.gnused
        inputs.nixpkgs.jq
      ];
    };
    entrypoint = ./data.sh;
  };
  dynamodb = makeDynamoDb {
    name = "db";
    host = "0.0.0.0";
    port = "8022";
    infra = projectPath "/integrates/db/dynamodb/infra";
    data = ["integrates/db/.data"];
    daemonMode = false;
  };
in
  makeScript {
    name = "dynamodb";
    searchPaths = {
      bin = [
        dynamodb_data
        dynamodb
      ];
    };
    entrypoint = ./entrypoint.sh;
  }
