{ makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  builder = path "/makes/packages/integrates/front/build-pkg/prod/builder.sh";
  name = "integrates-front-build-prod";
  searchPaths = {
    envSources = [
      packages.integrates.front.build-pkg
    ];
  };
}
