{ importUtility
, makes
, packages
, ...
}:
makes.makeScript {
  name = "skims-owasp-benchmark-and-upload";
  searchPaths = {
    bin = [
      packages.skims.owasp-benchmark
      packages.observes.tap-json
      packages.observes.target-redshift
    ];
    source = [
      (importUtility "aws")
      (importUtility "sops")
    ];
  };
  entrypoint = ./entrypoint.sh;
}
