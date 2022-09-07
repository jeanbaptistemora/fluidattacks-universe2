# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  outputs,
  inputs,
  makeScript,
  ...
}: let
  onAws = outputs."/computeOnAwsBatch/observesDynamoV2Etl";
  onAwsBig = outputs."/computeOnAwsBatch/observesDynamoV2EtlBig";
  parallelOnAws = outputs."/computeOnAwsBatch/observesDynamoParallel";
  prepareOnAws = outputs."/computeOnAwsBatch/observesDynamoPrepare";
in
  makeScript {
    searchPaths = {
      bin = [
        outputs."${inputs.observesIndex.etl.dynamo.bin}"
      ];
      source = [
        outputs."/observes/common/db-creds"
      ];
    };
    replace = {
      __argSendTableETL__ = "${onAws}/bin/${onAws.name}";
      __argSendBigTableETL__ = "${onAwsBig}/bin/${onAwsBig.name}";
      __argSendParallelTableETL__ = "${parallelOnAws}/bin/${parallelOnAws.name}";
      __argSendPrepare__ = "${prepareOnAws}/bin/${prepareOnAws.name}";
    };
    name = "observes-etl-dynamo-conf";
    entrypoint = ./entrypoint.sh;
  }
