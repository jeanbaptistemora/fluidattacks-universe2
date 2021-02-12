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
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/gitlab"
    ];
  };
  name = "observes-scheduled-timedoctor-refresh-token";
  template = path "/makes/applications/observes/scheduled-timedoctor-refresh-token/entrypoint.sh";
}
