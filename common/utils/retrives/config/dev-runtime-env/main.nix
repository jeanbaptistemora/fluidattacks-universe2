{
  makeNodeJsEnvironment,
  projectPath,
  ...
}:
makeNodeJsEnvironment {
  name = "retrieves-dev-runtime";
  nodeJsVersion = "18";
  packageJson = projectPath "/common/utils/retrives/package.json";
  packageLockJson = projectPath "/common/utils/retrives/package-lock.json";
}
