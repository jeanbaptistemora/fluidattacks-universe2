{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    source = [ outputs."/reviews/runtime" ];
  };
  name = "makes-review-mr";
  entrypoint = ./entrypoint.sh;
}
