{ makeScript
, outputs
, ...
}:
makeScript {
  name = "sorts";
  searchPaths = {
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
      outputs."/sorts/config-runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
