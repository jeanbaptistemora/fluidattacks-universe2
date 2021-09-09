{ makes
, path
, ...
}:
let
  nodeJsEnvironment = makes.makeNodeJsEnvironment {
    name = "makes-announce-bugsnag";
    nodeJsVersion = "12";
    packageJson = ./npm/package.json;
    packageLockJson = ./npm/package-lock.json;
  };
in
makes.makeScript {
  entrypoint = path "/makes/applications/makes/announce/bugsnag/entrypoint.sh";
  name = "makes-announce-bugsnag";
  searchPaths.source = [ nodeJsEnvironment ];
}
