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
  name = "observes-service-jobs-scheduler-env-runtime";
  searchPaths = {
    export = builtins.attrValues (builtins.mapAttrs
      (name: output: [ name output "/bin/${output.name}" ])
      {
        announceKitEtl = outputs."/computeOnAwsBatch/observesAnnounceKitEtl";
        bugsnagEtl = outputs."/computeOnAwsBatch/observesBugsnagEtl";
        checklyEtl = outputs."/computeOnAwsBatch/observesChecklyEtl";
        delightedEtl = outputs."/computeOnAwsBatch/observesDelightedEtl";
        dynamoDbForcesEtl = outputs."/computeOnAwsBatch/observesDynamoDbForcesEtl";
        formstackEtl = outputs."/computeOnAwsBatch/observesFormstackEtl";
        gitlabEtlChallenges = outputs."/computeOnAwsBatch/observesGitlabEtlChallenges";
        gitlabEtlDefault = outputs."/computeOnAwsBatch/observesGitlabEtlDefault";
        gitlabEtlProduct = outputs."/computeOnAwsBatch/observesGitlabEtlProduct";
        gitlabEtlServices = outputs."/computeOnAwsBatch/observesGitlabEtlServices";
        batchStability = outputs."/observes/job/batch-stability";
        codeEtlMirror = outputs."/observes/etl/code/mirror/all-on-aws";
        codeEtlUpload = outputs."/observes/etl/code/upload/all-on-aws";
        dynamoDbIntegratesEtl = outputs."/observes/etl/dynamo/integrates";
        dynamoTableEtlBig = outputs."/computeOnAwsBatch/observesDynamoTableEtlBig";
      });
    pythonMypy = [ self ];
    pythonPackage = [ self ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-service-jobs-scheduler-env-runtime-python";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/common/purity/env/runtime"
      outputs."${inputs.observesIndex.common.utils_logger.env.runtime}"
    ];
  };
}
