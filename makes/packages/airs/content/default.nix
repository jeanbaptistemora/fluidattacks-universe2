{ airsPkgs
, makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envAirsContent = path "/airs/content";
    envAirsNewFront = path "/airs/new-front";
    envAirsNpm = packages.airs.npm;
  };
  builder = path "/makes/packages/airs/content/builder.sh";
  name = "airs-content";
  searchPaths = {
    envPaths = [ airsPkgs.findutils ];
  };
}
