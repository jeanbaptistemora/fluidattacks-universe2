{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    source = [
      outputs."${inputs.observesIndex.tap.gitlab.bin}"
      outputs."${inputs.observesIndex.target.redshift.bin}"
    ];
  };
  name = "observes-etl-gitlab-ephemeral";
  entrypoint = ./entrypoint.sh;
}
