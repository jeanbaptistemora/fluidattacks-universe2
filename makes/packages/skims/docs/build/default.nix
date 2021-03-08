{ makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrcSkimsDocs = path "/skims/docs";
    envSrcSkimsReadme = path "/skims/README.md";
    envSrcSkimsSkims = path "/skims/skims";
  };
  builder = path "/makes/packages/skims/docs/build/builder.sh";
  name = "skims-docs-build";
  searchPaths = {
    envSources = [
      packages.skims.config-development
      packages.skims.config-runtime
    ];
  };
}
