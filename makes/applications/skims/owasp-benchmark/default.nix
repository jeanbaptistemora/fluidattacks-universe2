{ makes
, packages
, skimsBenchmarkOwaspRepo
, nixpkgs
, ...
}:
makes.makeScript {
  name = "skims-owasp-benchmark";
  replace = {
    __argBenchmarkRepo__ = skimsBenchmarkOwaspRepo;
  };
  searchPaths = {
    bin = [ nixpkgs.python38 packages.skims ];
    source = [ packages.skims.config-runtime ];
  };
  entrypoint = ./entrypoint.sh;
}
