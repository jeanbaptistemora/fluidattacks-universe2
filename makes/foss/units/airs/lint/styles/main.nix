{ inputs
, makeDerivation
, projectPath
, ...
}:
makeDerivation {
  env = {
    envAirsFront = projectPath "/airs/front";
    envAirsNpm = inputs.product.airs-npm;
  };
  builder = ./builder.sh;
  name = "airs-lint-styles";
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
    ];
    source = [ inputs.product.airs-npm-env ];
  };
}
