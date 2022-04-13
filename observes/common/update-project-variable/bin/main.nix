{
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    source = [
      outputs."/common/utils/gitlab"
    ];
  };
  name = "observes-common-update-project-variable-bin";
  entrypoint = ./entrypoint.sh;
}
