{
  inputs,
  outputs,
  ...
}: {
  dev = {
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
        outputs."/observes/service/jobs-scheduler/env/runtime"
      ];
    };
    observesCodeEtl = {
      source = [
        outputs."/observes/etl/code/env/development"
      ];
    };
    observesTapDynamo = {
      source = [
        outputs."/observes/singer/tap-dynamo/env/development"
      ];
    };
    observesEtlDynamoConf = {
      source = [
        outputs."${inputs.observesIndex.etl.dynamo.env.dev}"
      ];
    };
    observesCommonUtilsLogger = {
      source = [
        outputs."${inputs.observesIndex.common.utils_logger.new_env.dev}"
      ];
    };
    observesServiceDbMigration = {
      source = [
        outputs."${inputs.observesIndex.service.db_migration.env.dev}"
      ];
    };
  };
}
