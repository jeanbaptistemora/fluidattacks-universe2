{ makeDerivation
, makeNodeJsEnvironment
, projectPath
, ...
}:
let
  name = "integrates-charts-lint";
  nodeJsEnvironment = makeNodeJsEnvironment {
    inherit name;
    nodeJsVersion = "12";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
makeDerivation {
  builder = ./builder.sh;
  env.envSrc = projectPath "/integrates/back/src/app/templates/static/graphics";
  inherit name;
  searchPaths.source = [ nodeJsEnvironment ];
}
