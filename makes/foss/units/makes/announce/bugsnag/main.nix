{ makeNodeJsEnvironment
, makeScript
, ...
}:
let
  nodeJsEnvironment = makeNodeJsEnvironment {
    name = "makes-announce-bugsnag";
    nodeJsVersion = "12";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "makes-announce-bugsnag";
  searchPaths.source = [ nodeJsEnvironment ];
}
