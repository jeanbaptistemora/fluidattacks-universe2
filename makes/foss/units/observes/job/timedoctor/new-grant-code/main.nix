{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/service/timedoctor-tokens/bin"
    ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/sops"
    ];
  };
  name = "observes-job-timedoctor-new-grant-code";
  entrypoint = ./entrypoint.sh;
}
