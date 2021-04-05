{ nixpkgs
, packages
, path
, ...
}:
let
  nixPkgs = nixpkgs;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixPkgs;
in
makeEntrypoint {
  arguments = { };
  searchPaths = {
    envPaths = [
      nixPkgs.awscli
      nixPkgs.coreutils
      nixPkgs.jq
      packages.observes.bin.tap-timedoctor
      packages.observes.target-redshift
      packages.observes.update-sync-date
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/gitlab"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-timedoctor-etl";
  template = path "/makes/applications/observes/scheduled/timedoctor-etl/entrypoint.sh";
}
