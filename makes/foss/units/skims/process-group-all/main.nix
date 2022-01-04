{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  replace = {
    __argGetConfig__ = ./src/get_config.py;
  };
  name = "skims-process-group-all";
  searchPaths = {
    bin = [
      inputs.nixpkgs.jq
      inputs.nixpkgs.yq
      inputs.nixpkgs.parallel
      outputs."/melts"
      outputs."/skims"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/env"
      outputs."/utils/git"
      outputs."/utils/sops"
      outputs."/utils/time"
      outputs."/skims/config-runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
