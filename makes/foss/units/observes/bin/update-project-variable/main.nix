{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    source = [
      outputs."/utils/gitlab"
    ];
  };
  name = "observes-bin-update-project-variable";
  entrypoint = ./entrypoint.sh;
}
