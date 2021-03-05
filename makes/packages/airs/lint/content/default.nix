{ airsPkgs
, makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envAirs = path "/airs";
    envExclude = path "/makes/packages/airs/lint/content/exclude.lst";
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
