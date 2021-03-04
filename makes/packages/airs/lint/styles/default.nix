{ airsPkgs
, makeDerivation
, packages
, path
, ...
}:
makeDerivation airsPkgs {
  arguments = {
    envAirsNewFront = path "/airs/new-front";
    envAirsNpm = packages.airs.npm;
  };
  builder = path "/makes/packages/airs/lint/styles/builder.sh";
  name = "airs-lint-styles";
  searchPaths = {
    envPaths = [
      airsPkgs.findutils
    ];
  };
}
