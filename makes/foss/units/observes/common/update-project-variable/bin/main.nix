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
  name = "observes-common-update-project-variable-bin";
  entrypoint = ./entrypoint.sh;
}
