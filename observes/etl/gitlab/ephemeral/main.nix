{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.target.redshift.bin}"
      outputs."${inputs.observesIndex.tap.gitlab.bin}"
    ];
  };
  name = "observes-etl-gitlab-ephemeral";
  entrypoint = ./entrypoint.sh;
}
