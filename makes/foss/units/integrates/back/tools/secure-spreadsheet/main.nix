{ makeNodeJsEnvironment
, ...
}:
makeNodeJsEnvironment {
  name = "integrates-back-tools-secure-spreadsheet";
  nodeJsVersion = "14";
  packageJson = ./npm/package.json;
  packageLockJson = ./npm/package-lock.json;
}
