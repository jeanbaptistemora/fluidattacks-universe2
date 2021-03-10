{ makeEntrypoint
, nixpkgs
, packages
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
      packages.melts
      packages.observes.update-sync-date
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/git"
      "/makes/utils/sops"
    ];
  };
  name = "observes-job-code-etl-mirror";
  template = path "/makes/applications/observes/job/code-etl-mirror/entrypoint.sh";
}
