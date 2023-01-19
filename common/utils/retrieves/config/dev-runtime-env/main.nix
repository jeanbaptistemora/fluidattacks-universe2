{
  makeNodeJsEnvironment,
  projectPath,
  ...
}:
makeNodeJsEnvironment {
  name = "retrieves-dev-runtime";
  nodeJsVersion = "18";
  packageJson = projectPath "/common/utils/retrieves/package.json";
  packageLockJson = projectPath "/common/utils/retrieves/package-lock.json";
}
