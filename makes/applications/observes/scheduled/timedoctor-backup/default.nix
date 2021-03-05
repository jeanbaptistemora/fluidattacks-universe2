{ nixpkgs2
, packages
, path
, ...
}:
let
  nixPkgs = nixpkgs2;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixPkgs;
in
makeEntrypoint {
  arguments = { };
  searchPaths = {
    envPaths = [
      nixPkgs.awscli
      nixPkgs.coreutils
      nixPkgs.jq
      packages.observes.tap-timedoctor
      packages.observes.update-sync-date
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/gitlab"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-timedoctor-backup";
  template = path "/makes/applications/observes/scheduled/timedoctor-backup/entrypoint.sh";
}
