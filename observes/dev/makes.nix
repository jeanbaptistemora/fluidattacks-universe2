{
  inputs,
  outputs,
  ...
}: let
  products = with inputs.observesIndex; {
    observesCodeEtl = etl.code;
    observesBatchStability = service.batch_stability;
    observesServiceDbMigration = service.db_migration;
    observesTapCheckly = tap.checkly;
    observesEtlDynamoConf = etl.dynamo;
  };
  dev_envs =
    builtins.mapAttrs (
      _: v: {
        source = [outputs."${v.env.dev}"];
      }
    )
    products;
in {
  dev =
    dev_envs
    // {
      observesPaginator = {
        source = [
          outputs."/observes/common/paginator/env/development"
        ];
      };
      observesPostgresClient = {
        source = [
          outputs."/observes/common/postgres-client/env/development"
        ];
      };
      observesPurity = {
        source = [
          outputs."/observes/common/purity/env/development"
        ];
      };
      observesSingerIO = {
        source = [
          outputs."/observes/common/singer-io/env/development"
        ];
      };
      observesScheduler = {
        source = [
          outputs."/observes/service/jobs-scheduler/env/development"
        ];
      };
      observesTapDynamo = {
        source = [
          outputs."/observes/singer/tap-dynamo/env/development"
        ];
      };
      observesCommonUtilsLogger = {
        source = [
          outputs."${inputs.observesIndex.common.utils_logger.new_env.dev}"
        ];
      };
    };
}
