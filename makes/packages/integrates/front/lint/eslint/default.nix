{ integratesPkgs
, makeDerivation
, packages
, path
, ...
}:
makeDerivation integratesPkgs {
  arguments = {
    envBashLibCommon = path "/makes/utils/common/template.sh";
    envSetupIntegratesFrontDevRuntime = packages.integrates.front.config.dev-runtime;
    envSrcIntegratesFront = path "/integrates/front";
  };
  builder = path "/makes/packages/integrates/front/lint/eslint/builder.sh";
  name = "integrates-front-lint-eslint";
  searchPaths = {
    envPaths = [
      integratesPkgs.nodejs
      integratesPkgs.bash
    ];
  };
}
