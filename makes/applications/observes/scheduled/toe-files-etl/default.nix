{ makeUtils
, observesPkgs
, packages
, path
, ...
}:
makeUtils.makeEntrypoint observesPkgs {
  searchPaths = {
    envPaths = [
      packages.observes.tap-toe-files
      packages.observes.tap-json
      packages.observes.target-redshift
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/git"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-toe-files-etl";
  template = path "/makes/applications/observes/scheduled/toe-files-etl/entrypoint.sh";
}
