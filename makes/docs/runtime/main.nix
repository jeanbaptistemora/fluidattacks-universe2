{ makeNodeJsModules
, projectPath
, ...
}:
makeNodeJsModules {
  name = "docs-runtime";
  nodeJsVersion = "12";
  packageJson = projectPath "/makes/docs/runtime/npm/package.json";
  packageLockJson = projectPath "/makes/docs/runtime/npm/package-lock.json";
}
