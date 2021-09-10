{ makes
, ...
}:
let
  nodeJsEnvironment = makes.makeNodeJsEnvironment {
    name = "makes-bugsnag-source-map-uploader";
    nodeJsVersion = "12";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
makes.makeScript {
  name = "makes-bugsnag-source-map-uploader";
  searchPaths = {
    source = [ nodeJsEnvironment ];
  };
  entrypoint = ./entrypoint.sh;
}
