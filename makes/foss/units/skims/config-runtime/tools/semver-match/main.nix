{ makeNodeJsEnvironment
, makeScript
, projectPath
, ...
}:
let
  name = "skims-tools-semver-match";
  env = makeNodeJsEnvironment {
    inherit name;
    nodeJsVersion = "16";
    packageJson = projectPath "/skims/tools/semver-match/package.json";
    packageLockJson = projectPath "/skims/tools/semver-match/package-lock.json";
  };
in
makeScript {
  aliases = [ "semver-match" ];
  entrypoint = ./entrypoint.sh;
  inherit name;
  replace = {
    __argMatchJs__ = projectPath "/skims/tools/semver-match/index.js";
  };
  searchPaths.source = [ env ];
}
