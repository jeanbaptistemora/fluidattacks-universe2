{ makeNodeJsModules
, projectPath
, ...
}:
makeNodeJsModules {
  name = "docs-runtime";
  nodeJsVersion = "12";
  packageJson = projectPath "/makes/foss/units/docs/runtime/npm/package.json";
  packageLockJson = projectPath "/makes/foss/units/docs/runtime/npm/package-lock.json";
}
