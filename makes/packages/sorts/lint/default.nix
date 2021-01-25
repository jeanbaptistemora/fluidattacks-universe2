{ path
, sortsPkgs
, ...
} @ attrs:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path sortsPkgs;
in
makeDerivation {
  builder = path "/makes/packages/sorts/lint/builder.sh";
  envBashLibLintPython = import (path "/makes/utils/lint-python") path sortsPkgs;
  envImportLinterConfig = path "/sorts/setup.imports.cfg";
  envSetupSortsDevelopment = import (path "/makes/packages/sorts/config-development") attrs.copy;
  envSetupSortsRuntime = import (path "/makes/packages/sorts/config-runtime") attrs.copy;
  envSrcSortsSorts = path "/sorts/sorts";
  envSrcSortsTest = path "/sorts/test";
  envSrcSortsTraining = path "/sorts/training";
  name = "sorts-lint";
}
