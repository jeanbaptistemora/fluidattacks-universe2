{ packages
, path
, nixpkgs
, ...
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path nixpkgs;
in
makeDerivation {
  arguments = {
    envImportLinterConfig = path "/sorts/setup.imports.cfg";
    envSetupSortsDevelopment = packages.sorts.config-development;
    envSetupSortsRuntime = packages.sorts.config-runtime;
    envSrcSortsSorts = path "/sorts/sorts";
    envSrcSortsTest = path "/sorts/test";
    envSrcSortsTraining = path "/sorts/training";
  };
  builder = path "/makes/packages/sorts/lint/builder.sh";
  name = "sorts-lint";
  searchPaths = {
    envUtils = [ "/makes/utils/lint-python" ];
  };
}
