{ makeEntrypoint
, packages
, path
, nixpkgs
, ...
}:
makeEntrypoint {
  arguments = {
    envGetConfig = path "/makes/applications/skims/process-group/src/get_config.py";
  };
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
