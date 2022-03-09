{
  makeScript,
  inputs,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
      outputs."${inputs.observesIndex.service.db_migration.env.runtime}"
    ];
  };
  name = "observes-job-migration";
  entrypoint = ./entrypoint.sh;
}
