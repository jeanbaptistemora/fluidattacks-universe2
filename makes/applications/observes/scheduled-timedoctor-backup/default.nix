{ observesPkgs
, packages
, path
, ...
} @ _:
let
  nixPkgs = observesPkgs;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixPkgs;
in
makeEntrypoint {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages."observes/tap-timedoctor"
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
  name = "observes-scheduled-timedoctor-backup";
  template = path "/makes/applications/observes/scheduled-timedoctor-backup/entrypoint.sh";
}
