{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  replace = {
    __argGetConfig__ = ./src/get_config.py;
  };
  name = "skims-process-group";
  searchPaths = {
    bin = [
      inputs.nixpkgs.jq
      inputs.nixpkgs.yq
      outputs."/melts"
      outputs."/skims"
    ];
    source = [
      (outputs."/utils/aws")
      (inputs.legacy.importUtility "env")
      (outputs."/utils/git")
      (outputs."/utils/sops")
      (inputs.legacy.importUtility "time")
      outputs."/skims/config-runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
