{ makeScript
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-bin-tap-gitlab
      inputs.product.observes-tap-json
      inputs.product.observes-target-redshift
    ];
  };
  name = "observes-job-gitlab-etl";
  entrypoint = ./entrypoint.sh;
}
