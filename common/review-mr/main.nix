{
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    source = [outputs."/reviews/runtime"];
  };
  name = "common-review-mr";
  entrypoint = ./entrypoint.sh;
}
