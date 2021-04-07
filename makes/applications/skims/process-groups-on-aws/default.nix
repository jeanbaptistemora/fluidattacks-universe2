{ makeEntrypoint
, nixpkgs
, packages
, path
, ...
}:
makeEntrypoint {
  name = "skims-process-groups-on-aws";
  searchPaths = {
    envPaths = [
      nixpkgs.gnugrep
      packages.skims.process-group-on-aws
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/git"
    ];
  };
  template = path "/makes/applications/skims/process-groups-on-aws/entrypoint.sh";
}
