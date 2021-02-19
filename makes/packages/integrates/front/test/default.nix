{ integratesPkgs
, makeDerivation
, packages
, path
, ...
} @ _:
makeDerivation integratesPkgs {
  arguments = {
    envBashLibCommon = path "/makes/utils/common/template.sh";
    envSetupIntegratesFrontDevRuntime = packages.integrates.front.config.dev-runtime;
    envSrcIntegratesFront = path "/integrates/front";
  };
  builder = path "/makes/packages/integrates/front/test/builder.sh";
  name = "integrates-front-test";
  searchPaths = {
    envPaths = [
      integratesPkgs.bash
      integratesPkgs.nodejs
    ];
  };
}
