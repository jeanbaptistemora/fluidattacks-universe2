{ makes
, ...
}:
makes.makeNodeJsEnvironment {
  name = "integrates-back-tools-secure-spreadsheet";
  nodeJsVersion = "12";
  packageJson = ./npm/package.json;
  packageLockJson = ./npm/package-lock.json;
}
