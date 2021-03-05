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
    envBashLibLintPython = import (path "/makes/utils/lint-python") path nixpkgs;
    envImportLinterConfig = path "/sorts/setup.imports.cfg";
    envSetupSortsDevelopment = packages.sorts.config-development;
    envSetupSortsRuntime = packages.sorts.config-runtime;
    envSrcSortsSorts = path "/sorts/sorts";
    envSrcSortsTest = path "/sorts/test";
    envSrcSortsTraining = path "/sorts/training";
  };
  builder = path "/makes/packages/sorts/lint/builder.sh";
  name = "sorts-lint";
}
