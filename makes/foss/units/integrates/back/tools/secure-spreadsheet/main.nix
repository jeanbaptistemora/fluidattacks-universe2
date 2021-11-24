{ makeNodeJsEnvironment
, ...
}:
makeNodeJsEnvironment {
  name = "integrates-back-tools-secure-spreadsheet";
  nodeJsVersion = "16";
  packageJson = ./npm/package.json;
  packageLockJson = ./npm/package-lock.json;
}
