{ makeNodeJsModules
, projectPath
, ...
}:
makeNodeJsModules {
  name = "integrates-front-dev-runtime";
  nodeJsVersion = "12";
  packageJson = projectPath "/integrates/front/package.json";
  packageLockJson = projectPath "/integrates/front/package-lock.json";
}
