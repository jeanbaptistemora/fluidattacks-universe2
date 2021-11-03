{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/service/job-last-success"
      outputs."/observes/bin/service/timedoctor-tokens"
    ];
    source = [
      (outputs."/utils/aws")
      (inputs.legacy.importUtility "gitlab")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-timedoctor-refresh-token";
  entrypoint = ./entrypoint.sh;
}
