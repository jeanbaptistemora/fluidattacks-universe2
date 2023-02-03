{
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "forces";
  searchPaths = {
    source = [outputs."/integrates/forces/config/runtime"];
  };
  entrypoint = ./entrypoint.sh;
}
