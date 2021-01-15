{ sortsPkgs
, ...
} @ attrs:
let
  config = import ../../../makes/sorts/config attrs.copy;
  makeDerivation = import ../../../makes/utils/make-derivation sortsPkgs;
in
makeDerivation {
  builder = ./builder.sh;
  envBashLibLintPython = import ../../../makes/utils/bash-lib/lint-python sortsPkgs;
  envImportLinterConfig = ../../../sorts/setup.imports.cfg;
  envSetupSortsDevelopment = config.setupSortsDevelopment;
  envSetupSortsRuntime = config.setupSortsRuntime;
  envSrcSortsSorts = ../../../sorts/sorts;
  envSrcSortsTest = ../../../sorts/test;
  envSrcSortsTraining = ../../../sorts/training;
  name = "sorts-lint";
}
