{ makeEntrypoint
, packages
, path
, nixpkgs
, ...
}:
makeEntrypoint {
  name = "skims-process-group";
  searchPaths = {
    envPaths = [
      packages.melts
      packages.observes.bin.service.job-last-success
      packages.skims
      nixpkgs.jq
      nixpkgs.yq
    ];
    envSources = [
      packages.skims.config-runtime
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/git"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/skims/process-group/entrypoint.sh";
}
