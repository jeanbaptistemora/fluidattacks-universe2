{ makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrcMeltsToolbox = path "/melts/toolbox";
    envSrcMeltsTest = path "/melts/tests";
  };
  builder = path "/makes/packages/melts/lint/builder.sh";
  name = "melts-lint";
  searchPaths = {
    envSources = [
      packages.melts.config-development
      packages.melts.config-runtime
    ];
    envUtils = [ "/makes/utils/lint-python" ];
  };
}
