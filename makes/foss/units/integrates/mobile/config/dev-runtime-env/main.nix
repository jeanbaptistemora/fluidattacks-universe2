{ inputs
, makeNodeJsEnvironment
, projectPath
, ...
}:
makeNodeJsEnvironment {
  name = "integrates-mobile-dev-runtime";
  nodeJsVersion = "12";
  searchPaths.bin = [
    inputs.nixpkgs.bash
    inputs.nixpkgs.gcc
    inputs.nixpkgs.gnugrep
    inputs.nixpkgs.gnumake
    inputs.nixpkgs.gnused
    inputs.nixpkgs.python39
  ];
  packageJson = projectPath "/integrates/mobile/package.json";
  packageLockJson = projectPath "/integrates/mobile/package-lock.json";
}
