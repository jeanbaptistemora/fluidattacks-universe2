{ makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  searchPaths = {
    source = [ outputs."/reviews/runtime" ];
  };
  name = "makes-review-mr";
  entrypoint = projectPath "/makes/foss/units/makes/review-mr/entrypoint.sh";
}
