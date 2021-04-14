{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  name = "skims-owasp-benchmark-and-upload";
  searchPaths = {
    envPaths = [
      packages.skims.owasp-benchmark
      packages.observes.tap-json
      packages.observes.target-redshift
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/skims/owasp-benchmark-and-upload/entrypoint.sh";
}
