{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/tap-gitlab"
      outputs."/observes/bin/tap-json"
      inputs.product.observes-target-redshift
    ];
  };
  name = "observes-job-gitlab-etl";
  entrypoint = ./entrypoint.sh;
}
