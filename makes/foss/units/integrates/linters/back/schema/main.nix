{ makeDerivation
, makeNodeJsEnvironment
, projectPath
, ...
}:
let
  nodeJsEnvironment = makeNodeJsEnvironment {
    name = "integrates-linters-back-schema";
    nodeJsVersion = "14";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
makeDerivation {
  builder = ./builder.sh;
  env.envIntegratesApiSchema = projectPath "/integrates/back/src/api/schema";
  name = "integrates-linters-back-schema";
  searchPaths.source = [ nodeJsEnvironment ];
}
