{ makeEntrypoint
, path
, packages
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.target-redshift
      packages.observes.tap-json
      packages.observes.bin.tap-mailchimp

    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-job-mailchimp-etl";
  template = path "/makes/applications/observes/scheduled/job/mailchimp-etl/entrypoint.sh";
}
