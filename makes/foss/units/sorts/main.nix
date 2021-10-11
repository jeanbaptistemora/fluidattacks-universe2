{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  name = "sorts";
  searchPaths = {
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
      outputs."/sorts/config-runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
