{ makeEntrypoint
, observesPkgs
, path
, packages
, ...
}:
makeEntrypoint observesPkgs {
  searchPaths = {
    envPaths = [
      packages.observes.target-redshift
      packages.observes.tap-json
      packages.observes.tap-mailchimp

    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-mailchimp-etl";
  template = path "/makes/applications/observes/scheduled/mailchimp-etl/entrypoint.sh";
}
