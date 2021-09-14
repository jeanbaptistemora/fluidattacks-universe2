{ nixpkgs
, makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envAirsFront = path "/airs/front";
    envAirsNpm = packages.airs.npm;
  };
  builder = path "/makes/packages/airs/lint/styles/builder.sh";
  name = "airs-lint-styles";
  searchPaths = {
    envPaths = [
      nixpkgs.findutils
    ];
    envSources = [ packages.airs.npm.env ];
  };
}
