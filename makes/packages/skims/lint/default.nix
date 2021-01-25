{ path
, skimsPkgs
, ...
} @ attrs:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  builder = path "/makes/packages/skims/lint/builder.sh";
  envBashLibLintPython = import (path "/makes/utils/lint-python") path skimsPkgs;
  envImportLinterConfig = path "/skims/setup.imports.cfg";
  envSetupSkimsDevelopment = import (path "/makes/packages/skims/config-development") attrs.copy;
  envSetupSkimsRuntime = import (path "/makes/packages/skims/config-runtime") attrs.copy;
  envSrcSkimsSkims = path "/skims/skims";
  envSrcSkimsTest = path "/skims/test";
  name = "skims-lint";
}
