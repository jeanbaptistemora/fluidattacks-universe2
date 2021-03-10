{ nixpkgs
, makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envAirsContent = path "/airs/content";
    envAirsImages = path "/airs/theme/2020/static/images";
    envAirsNewFront = path "/airs/new-front";
    envAirsNpm = packages.airs.npm;
  };
  builder = path "/makes/packages/airs/content/builder.sh";
  name = "airs-content";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
      nixpkgs.gnused
    ];
  };
}
