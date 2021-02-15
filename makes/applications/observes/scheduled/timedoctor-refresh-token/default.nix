{ makeEntrypoint
, observesPkgs
, packages
, path
, ...
} @ _:
makeEntrypoint observesPkgs {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages."observes/service/timedoctor-tokens"
      packages."observes/update-sync-date"
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/gitlab"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-timedoctor-refresh-token";
  template = path "/makes/applications/observes/scheduled/timedoctor-refresh-token/entrypoint.sh";
}
