{ inputs
, makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
let
  self = projectPath "/observes/services/jobs_scheduler";
in
makeTemplate {
  name = "observes-env-service-jobs-scheduler-runtime";
  searchPaths = {
    export = builtins.attrValues (builtins.mapAttrs
      (name: output: [ name output "/bin/${output.name}" ])
      {
        bugsnagEtl = outputs."/computeOnAwsBatch/observesBugsnagEtl";
        checklyEtl = outputs."/computeOnAwsBatch/observesChecklyEtl";
      });
    bin = [
      inputs.product.observes-job-batch-stability
      inputs.product.observes-scheduled-on-aws-code-etl-amend
      inputs.product.observes-scheduled-on-aws-code-etl-mirror
      inputs.product.observes-scheduled-on-aws-code-etl-upload
      inputs.product.observes-scheduled-on-aws-delighted-etl
      inputs.product.observes-scheduled-on-aws-dynamodb-forces-etl
      inputs.product.observes-scheduled-on-aws-dynamodb-integrates-etl
      inputs.product.observes-scheduled-on-aws-formstack-etl
      inputs.product.observes-scheduled-on-aws-gitlab-etl-challenges
      inputs.product.observes-scheduled-on-aws-gitlab-etl-default
      inputs.product.observes-scheduled-on-aws-gitlab-etl-product
      inputs.product.observes-scheduled-on-aws-gitlab-etl-services
    ];
    pythonMypy = [ self ];
    pythonPackage = [ self ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-service-jobs-scheduler-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      inputs.product.observes-env-utils-logger-runtime
    ];
  };
}
