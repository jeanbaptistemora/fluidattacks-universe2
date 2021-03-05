{ nixpkgs
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
  builder = path "/makes/packages/integrates/front/lint/tslint/builder.sh";
  name = "integrates-front-lint-tslint";
  searchPaths = {
    envPaths = [
      nixpkgs.nodejs
      nixpkgs.bash
    ];
  };
}
