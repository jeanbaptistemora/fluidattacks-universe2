{ makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envImportLinterConfig = path "/sorts/setup.imports.cfg";
    envSrcSortsSorts = path "/sorts/sorts";
    envSrcSortsTest = path "/sorts/test";
    envSrcSortsTraining = path "/sorts/training";
  };
  builder = path "/makes/packages/sorts/lint/builder.sh";
  name = "sorts-lint";
  searchPaths = {
    envSources = [
      packages.sorts.config-development
      packages.sorts.config-runtime
    ];
    envUtils = [ "/makes/utils/lint-python" ];
  };
}
