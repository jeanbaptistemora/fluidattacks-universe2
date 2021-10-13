{ makeScript
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [ inputs.product.observes-job-gitlab-etl ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-job-gitlab-etl-services";
  entrypoint = ./entrypoint.sh;
}
