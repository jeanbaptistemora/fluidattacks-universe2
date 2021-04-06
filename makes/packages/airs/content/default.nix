{ nixpkgs
, makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envAirsContent = path "/airs/content";
    envAirsContentImages = path "/airs/content/images";
    envAirsContentPages = path "/airs/content/pages";
    envAirsImages = path "/airs/theme/2020/static/images";
    envAirsNewFront = path "/airs/new-front";
    envAirsNpm = packages.airs.npm;
  };
  builder = path "/makes/packages/airs/content/builder.sh";
  name = "airs-content";
  searchPaths = {
    envLibraries = [
      nixpkgs.musl
    ];
    envPaths = [
      nixpkgs.findutils
      nixpkgs.gnused
    ];
  };
}
