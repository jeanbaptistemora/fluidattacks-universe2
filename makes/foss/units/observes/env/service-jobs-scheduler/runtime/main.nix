{ makePythonPypiEnvironment
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
        announceKitEtl = outputs."/computeOnAwsBatch/observesAnnounceKitEtl";
        bugsnagEtl = outputs."/computeOnAwsBatch/observesBugsnagEtl";
        checklyEtl = outputs."/computeOnAwsBatch/observesChecklyEtl";
        codeEtlAmend = outputs."/computeOnAwsBatch/observesCodeEtlAmend";
        delightedEtl = outputs."/computeOnAwsBatch/observesDelightedEtl";
        dynamoDbForcesEtl = outputs."/computeOnAwsBatch/observesDynamoDbForcesEtl";
        formstackEtl = outputs."/computeOnAwsBatch/observesFormstackEtl";
        gitlabEtlChallenges = outputs."/computeOnAwsBatch/observesGitlabEtlChallenges";
        gitlabEtlDefault = outputs."/computeOnAwsBatch/observesGitlabEtlDefault";
        gitlabEtlProduct = outputs."/computeOnAwsBatch/observesGitlabEtlProduct";
        gitlabEtlServices = outputs."/computeOnAwsBatch/observesGitlabEtlServices";
        batchStability = outputs."/observes/job/batch-stability";
        codeEtlMirror = outputs."/observes/scheduled/on-aws/code-etl-mirror";
        codeEtlUpload = outputs."/observes/scheduled/on-aws/code-etl-upload";
        dynamoDbIntegratesEtl = outputs."/observes/scheduled/on-aws/dynamodb-integrates-etl";
      });
    pythonMypy = [ self ];
    pythonPackage = [ self ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-service-jobs-scheduler-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/utils-logger/runtime"
    ];
  };
}
