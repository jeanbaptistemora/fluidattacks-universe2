{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  name = "sorts";
  searchPaths = {
    source = [
      (outputs."/utils/aws")
      (inputs.legacy.importUtility "sops")
      outputs."/sorts/config-runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
