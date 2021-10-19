{ makeScript
, inputs
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      outputs."/observes/bin/tap-gitlab"
      inputs.product.observes-tap-json
      inputs.product.observes-target-redshift
    ];
  };
  name = "observes-job-gitlab-etl";
  entrypoint = ./entrypoint.sh;
}
