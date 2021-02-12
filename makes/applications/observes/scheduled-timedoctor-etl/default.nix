{ applications
, observesPkgs
, path
, ...
} @ _:
let
  nixPkgs = observesPkgs;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixPkgs;
in
makeEntrypoint {
  arguments = {
    envTapTimedoctor = applications."observes/tap-timedoctor";
    envTargetRedshift = applications."observes/target-redshift";
  };
  searchPaths = {
    envPaths = [
      nixPkgs.awscli
      nixPkgs.coreutils
      nixPkgs.jq
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/gitlab"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-timedoctor-etl";
  template = path "/makes/applications/observes/scheduled-timedoctor-etl/entrypoint.sh";
}
