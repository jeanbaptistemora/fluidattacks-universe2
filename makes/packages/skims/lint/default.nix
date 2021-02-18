{ packages
, path
, skimsPkgs
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  builder = path "/makes/packages/skims/lint/builder.sh";
  envBashLibLintPython = import (path "/makes/utils/lint-python") path skimsPkgs;
  envImportLinterConfig = path "/skims/setup.imports.cfg";
  envSetupSkimsDevelopment = packages.skims.config-development;
  envSetupSkimsRuntime = packages.skims.config-runtime;
  envSrcSkimsSkims = path "/skims/skims";
  envSrcSkimsTest = path "/skims/test";
  name = "skims-lint";
}
