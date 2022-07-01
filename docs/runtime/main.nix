{
  makeNodeJsModules,
  projectPath,
  ...
}:
makeNodeJsModules {
  name = "docs-runtime";
  nodeJsVersion = "16";
  packageJson = projectPath "/docs/src/package.json";
  packageLockJson = projectPath "/docs/src/package-lock.json";
}
