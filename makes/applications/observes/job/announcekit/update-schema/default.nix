{ makeEntrypoint
, path
, packages
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.tap-announcekit
    ];
  };
  name = "observes-job-announcekit-update-schema";
  template = path "/makes/applications/observes/job/announcekit/update-schema/entrypoint.sh";
}
