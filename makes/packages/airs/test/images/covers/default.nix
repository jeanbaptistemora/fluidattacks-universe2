{ nixpkgs
, makeDerivation
, path
, ...
}:
makeDerivation {
  arguments = {
    envAirs = path "/airs";
  };
  builder = path "/makes/packages/airs/test/images/covers/builder.sh";
  name = "airs-test-images-covers";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
      nixpkgs.imagemagick
    ];
  };
}
