{ makes
, path
, ...
}:
makes.makeNodeJsModules {
  name = "airs-npm";
  nodeJsVersion = "12";
  packageJson = path "/airs/front/package.json";
  packageLockJson = path "/airs/front/package-lock.json";
  shouldIgnoreScripts = true;
}
