{ outputs
, ...
}:
{
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
  };
}
