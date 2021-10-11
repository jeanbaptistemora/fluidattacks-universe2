{ inputs
, makeScript
, ...
}:
makeScript {
  name = "sorts";
  searchPaths = {
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
      inputs.product.sorts-config-runtime
    ];
  };
  entrypoint = ./entrypoint.sh;
}
