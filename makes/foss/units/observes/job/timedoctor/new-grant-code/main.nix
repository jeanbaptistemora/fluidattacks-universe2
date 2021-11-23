{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/service/timedoctor-tokens"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  name = "observes-job-timedoctor-new-grant-code";
  entrypoint = ./entrypoint.sh;
}
