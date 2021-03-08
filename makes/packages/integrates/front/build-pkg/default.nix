{ nixpkgs
, makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envSetupIntegratesFrontDevRuntime = packages.integrates.front.config.dev-runtime;
    envIntegratesFront = path "/integrates/front";
    envJqueryCommentsPatch = path "/makes/packages/integrates/front/build-pkg/jquery-comments.diff";
  };
  builder = path "/makes/packages/integrates/front/build-pkg/builder.sh";
  name = "integrates-front-build-pkg";
  searchPaths = {
    envPaths = [
      nixpkgs.nodejs
      nixpkgs.patch
      nixpkgs.bash
    ];
  };
}
