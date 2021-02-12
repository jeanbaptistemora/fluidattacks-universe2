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
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixPkgs;
    envUtilsGitlab = import (path "/makes/utils/gitlab") path nixPkgs;
  };
  searchPaths = {
    envPaths = [
      nixPkgs.awscli
      nixPkgs.coreutils
      nixPkgs.jq
    ];
  };
  name = "observes-scheduled-timedoctor-etl";
  template = path "/makes/applications/observes/scheduled-timedoctor-etl/entrypoint.sh";
}
