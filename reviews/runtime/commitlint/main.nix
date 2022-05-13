{makeNodeJsEnvironment, ...}:
makeNodeJsEnvironment {
  name = "commitlint";
  nodeJsVersion = "14";
  packageJson = ./npm/package.json;
  packageLockJson = ./npm/package-lock.json;
}
