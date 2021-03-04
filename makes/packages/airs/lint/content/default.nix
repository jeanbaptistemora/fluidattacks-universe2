{ airsPkgs
, makeDerivation
, packages
, path
, ...
}:
makeDerivation airsPkgs {
  arguments = {
    envAirs = path "/airs";
  };
  builder = path "/makes/packages/airs/lint/content/builder.sh";
  name = "airs-lint-content";
  searchPaths = {
    envPaths = [
      airsPkgs.findutils
    ];
    envSources = [
      packages.airs.adoc.linter
    ];
  };
}
