{ makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envImportLinterConfig = path "/skims/setup.imports.cfg";
    envSrcSkimsSkims = path "/skims/skims";
    envSrcSkimsTest = path "/skims/test";
  };
  builder = path "/makes/packages/skims/lint/builder.sh";
  name = "skims-lint";
  searchPaths = {
    envSources = [
      packages.skims.config-development
      packages.skims.config-runtime
    ];
    envUtils = [ "/makes/utils/lint-python" ];
  };
}
