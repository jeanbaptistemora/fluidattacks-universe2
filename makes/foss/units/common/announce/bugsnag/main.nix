{
  makeNodeJsEnvironment,
  makeScript,
  ...
}: let
  nodeJsEnvironment = makeNodeJsEnvironment {
    name = "common-announce-bugsnag";
    nodeJsVersion = "12";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
  makeScript {
    entrypoint = ./entrypoint.sh;
    name = "common-announce-bugsnag";
    searchPaths.source = [nodeJsEnvironment];
  }
