{
  inputs,
  makeNodeJsVersion,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "docs";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.xdg_utils
      outputs."/docs/generate/criteria"
      outputs."/docs/generate/graphs"
      (makeNodeJsVersion "16")
    ];
  };
  entrypoint = ./entrypoint.sh;
}
