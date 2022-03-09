{
  makeNodeJsEnvironment,
  projectPath,
  ...
}:
makeNodeJsEnvironment {
  name = "airs-npm";
  nodeJsVersion = "14";
  packageJson = projectPath "/airs/front/package.json";
  packageLockJson = projectPath "/airs/front/package-lock.json";
  shouldIgnoreScripts = true;
}
