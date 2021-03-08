{ makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrcSkimsSkims = path "/skims/skims";
  };
  builder = path "/makes/packages/skims/structure/builder.sh";
  name = "skims-structure";
  searchPaths = {
    envSources = [
      packages.skims.config-development
      packages.skims.config-runtime
    ];
  };
}
