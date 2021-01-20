{ path
, sortsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/sorts/config") attrs.copy;
  makeDerivation = import (path "/makes/utils/make-derivation") path sortsPkgs;
in
makeDerivation {
  builder = path "/makes/sorts/lint/builder.sh";
  envBashLibLintPython = import (path "/makes/utils/bash-lib/lint-python") path sortsPkgs;
  envImportLinterConfig = path "/sorts/setup.imports.cfg";
  envSetupSortsDevelopment = config.setupSortsDevelopment;
  envSetupSortsRuntime = config.setupSortsRuntime;
  envSrcSortsSorts = path "/sorts/sorts";
  envSrcSortsTest = path "/sorts/test";
  envSrcSortsTraining = path "/sorts/training";
  name = "sorts-lint";
}
