{ makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  builder = path "/makes/packages/integrates/front/build-pkg/dev/builder.sh";
  name = "integrates-front-build-dev";
  searchPaths = {
    envSources = [
      packages.integrates.front.build-pkg
    ];
  };
}
