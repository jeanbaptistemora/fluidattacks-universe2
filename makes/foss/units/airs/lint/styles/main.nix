{ inputs
, makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  env = {
    envAirsFront = projectPath "/airs/front";
    envAirsNpm = outputs."/airs/npm";
  };
  builder = ./builder.sh;
  name = "airs-lint-styles";
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
    ];
    source = [ outputs."/airs/npm/env" ];
  };
}
