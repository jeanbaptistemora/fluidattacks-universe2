{
  makeNodeJsEnvironment,
  projectPath,
  ...
}:
makeNodeJsEnvironment {
  name = "integrates-front-dev-runtime";
  nodeJsVersion = "18";
  packageJson = projectPath "/integrates/front/package.json";
  packageLockJson = projectPath "/integrates/front/package-lock.json";
}
