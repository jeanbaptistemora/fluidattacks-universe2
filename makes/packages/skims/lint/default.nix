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
    envImportLinterConfig = path "/skims/setup.imports.cfg";
    envSetupSkimsDevelopment = packages.skims.config-development;
    envSetupSkimsRuntime = packages.skims.config-runtime;
    envSrcSkimsSkims = path "/skims/skims";
    envSrcSkimsTest = path "/skims/test";
  };
  builder = path "/makes/packages/skims/lint/builder.sh";
  name = "skims-lint";
}
