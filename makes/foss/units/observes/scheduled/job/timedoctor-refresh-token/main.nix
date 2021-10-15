{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/service/job-last-success"
      inputs.product.observes-bin-service-timedoctor-tokens
    ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "gitlab")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-scheduled-job-timedoctor-refresh-token";
  entrypoint = ./entrypoint.sh;
}
