{
  inputs,
  outputs,
  ...
}: let
  products = with inputs.observesIndex; {
    observesCodeEtl = etl.code;
    observesAsmDal = common.asm_dal;
    observesBatchStability = service.batch_stability;
    observesServiceDbMigration = service.db_migration;
    observesServiceSuccessIndicators = service.success_indicators;
    observesScheduler = service.scheduler;
    observesTapCheckly = tap.checkly;
    observesTapBugsnag = tap.bugsnag;
    observesTapDynamo = tap.dynamo;
    observesTapGitlab = tap.gitlab;
    observesTapJson = tap.json;
    observesTapMandrill = tap.mandrill;
    observesTargetRedshift = target.redshift_2;
    observesTargetS3 = target.s3;
    observesEtlDynamoConf = etl.dynamo;
    observesUtilsLogger2 = common.utils_logger_2;
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
      observesCommonUtilsLogger = {
        source = [
          outputs."${inputs.observesIndex.common.utils_logger.new_env.dev}"
        ];
      };
    };
}
