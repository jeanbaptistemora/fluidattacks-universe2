{ makeDerivation
, nixpkgs
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrc = path "/makes/applications/makes/criteria/src/";
  };
  builder = path "/makes/packages/makes/lint/criteria/builder.sh";
  name = "makes-lint-criteria";
  searchPaths = {
    envPaths = [
      nixpkgs.git
    ];
    envNodeBinaries = [
      packages.makes.ajv
    ];
    envNodeLibraries = [
      packages.makes.ajv
    ];
  };
}
