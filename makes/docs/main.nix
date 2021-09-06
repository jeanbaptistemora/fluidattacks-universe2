{ inputs
, makeNodeJsVersion
, makeScript
, outputs
, ...
}:
makeScript {
  name = "docs";
  replace = {
    __argNodeModules__ = outputs."/docs/runtime";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.xdg_utils
      outputs."/docs/generate/criteria"
      (makeNodeJsVersion "12")
    ];
    nodeBin = [ outputs."/docs/runtime" ];
    nodeModule = [ "./node_modules" ];
  };
  entrypoint = ./entrypoint.sh;
}
