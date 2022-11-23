{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."${inputs.observesIndex.tap.gitlab.bin}"
    ];
  };
  name = "observes-job-cancel-ci-jobs";
  entrypoint = ./entrypoint.sh;
}
