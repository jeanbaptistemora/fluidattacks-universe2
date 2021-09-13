{ makeEntrypoint
, path
, packages
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.tap-announcekit
      packages.observes.bin.service.job-last-success
      packages.observes.tap-json
      packages.observes.target-redshift
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-job-announcekit-etl";
  template = path "/makes/applications/observes/job/announcekit/etl/entrypoint.sh";
}
