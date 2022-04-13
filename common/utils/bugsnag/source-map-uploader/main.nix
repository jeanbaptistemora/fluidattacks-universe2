{
  makeNodeJsEnvironment,
  makeScript,
  ...
}: let
  nodeJsEnvironment = makeNodeJsEnvironment {
    name = "bugsnag-source-map-uploader";
    nodeJsVersion = "12";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
  makeScript {
    name = "bugsnag-source-map-uploader";
    searchPaths = {
      source = [nodeJsEnvironment];
    };
    entrypoint = ./entrypoint.sh;
  }
