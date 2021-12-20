{ makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/service/jobs-scheduler/bin"
    ];
    source = [
      outputs."/utils/aws"
    ];
  };
  name = "observes-service-jobs-scheduler-run";
  entrypoint = ./entrypoint.sh;
}
