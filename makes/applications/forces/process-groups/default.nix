{ makeEntrypoint
, packages
, nixpkgs
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      nixpkgs.jq
      packages.forces
    ];
    envSources = [
      packages.melts.lib
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "forces-process-groups";
  template = path "/makes/applications/forces/process-groups/entrypoint.sh";
}
