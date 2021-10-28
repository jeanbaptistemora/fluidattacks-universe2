{ makeNodeJsEnvironment
, ...
}:
makeNodeJsEnvironment {
  name = "commitlint";
  nodeJsVersion = "12";
  packageJson = ./npm/package.json;
  packageLockJson = ./npm/package-lock.json;
}
