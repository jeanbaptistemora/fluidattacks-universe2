{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    source = [ outputs."/reviews/runtime" ];
  };
  name = "reviews";
  entrypoint = ./entrypoint.sh;
}
