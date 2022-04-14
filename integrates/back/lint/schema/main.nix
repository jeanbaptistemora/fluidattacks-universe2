{
  makeDerivation,
  makeNodeJsEnvironment,
  projectPath,
  ...
}: let
  name = "integrates-back-lint-schema";
  nodeJsEnvironment = makeNodeJsEnvironment {
    inherit name;
    nodeJsVersion = "14";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
  makeDerivation {
    builder = ./builder.sh;
    env.envIntegratesApiSchema = projectPath "/integrates/back/src/api/schema";
    inherit name;
    searchPaths.source = [nodeJsEnvironment];
  }
