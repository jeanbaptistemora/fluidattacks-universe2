{
  makeDerivation,
  makeNodeJsEnvironment,
  projectPath,
  ...
}: let
  name = "integrates-back-lint-charts";
  nodeJsEnvironment = makeNodeJsEnvironment {
    inherit name;
    nodeJsVersion = "14";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
  makeDerivation {
    builder = ./builder.sh;
    env.envSrc = projectPath "/integrates/back/src/app/templates/static/graphics";
    inherit name;
    searchPaths.source = [nodeJsEnvironment];
  }
