{
  makeNodeJsEnvironment,
  makeScript,
  ...
}: let
  nodeJsEnvironment = makeNodeJsEnvironment {
    name = "common-bugsnag-source-map-uploader";
    nodeJsVersion = "12";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
  makeScript {
    name = "common-bugsnag-source-map-uploader";
    searchPaths = {
      source = [nodeJsEnvironment];
    };
    entrypoint = ./entrypoint.sh;
  }
