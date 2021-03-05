{ nixpkgs2
, makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envBashLibCommon = path "/makes/utils/common/template.sh";
    envSetupIntegratesFrontDevRuntime = packages.integrates.front.config.dev-runtime;
    envSrcIntegratesFront = path "/integrates/front";
  };
  builder = path "/makes/packages/integrates/front/lint/eslint/builder.sh";
  name = "integrates-front-lint-eslint";
  searchPaths = {
    envPaths = [
      nixpkgs2.nodejs
      nixpkgs2.bash
    ];
  };
}
