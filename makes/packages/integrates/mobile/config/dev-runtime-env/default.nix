{ makes
, nixpkgs
, path
, ...
}:
makes.makeNodeJsEnvironment {
  name = "integrates-mobile-dev-runtime";
  nodeJsVersion = "12";
  searchPaths.bin = [
    nixpkgs.bash
    nixpkgs.gcc
    nixpkgs.gnugrep
    nixpkgs.gnumake
    nixpkgs.gnused
    nixpkgs.python37
  ];
  packageJson = path "/integrates/mobile/package.json";
  packageLockJson = path "/integrates/mobile/package-lock.json";
}
