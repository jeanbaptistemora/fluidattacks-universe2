{ makes
, path
, ...
}:
makes.makeNodeJsEnvironment {
  name = "integrates-front-dev-runtime";
  nodeJsVersion = "12";
  packageJson = path "/integrates/front/package.json";
  packageLockJson = path "/integrates/front/package-lock.json";
}
