{
  makeNodeJsModules,
  projectPath,
  ...
}:
makeNodeJsModules {
  name = "airs-npm";
  nodeJsVersion = "18";
  packageJson = projectPath "/airs/front/package.json";
  packageLockJson = projectPath "/airs/front/package-lock.json";
  shouldIgnoreScripts = true;
}
