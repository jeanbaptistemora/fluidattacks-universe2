{ makeNodeJsModules
, projectPath
, ...
}:
makeNodeJsModules {
  name = "docs-runtime";
  nodeJsVersion = "12";
  packageJson = projectPath "/docs/src/package.json";
  packageLockJson = projectPath "/docs/src/package-lock.json";
}
