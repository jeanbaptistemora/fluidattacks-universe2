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
      inputs.product.melts
      inputs.nixpkgs.jq
      inputs.nixpkgs.yq
      outputs."/skims"
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "env")
      (inputs.legacy.importUtility "git")
      (inputs.legacy.importUtility "sops")
      (inputs.legacy.importUtility "time")
      outputs."/skims/config-runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
