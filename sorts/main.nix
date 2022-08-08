{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "sorts";
  searchPaths = {
    source = [
      outputs."/common/utils/sops"
      outputs."/sorts/config/runtime"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
