{ outputs
, ...
}:
{
  computeOnAwsBatch = {
    integratesSchedulerUpdateIndicators = {
      allowDuplicates = false;
      attempts = 1;
      attemptDurationSeconds = 43200;
      command = [
        "m"
        "gitlab:fluidattacks/product@master"
        "/legacy/integrates-scheduler-update-indicators-job"
      ];
      definition = "makes";
      includePositionalArgsInName = true;
      environment = [ "PRODUCT_API_TOKEN" ];
      memory = 1800;
      queue = "dedicated_later";
      setup = [
        outputs."/secretsForAwsFromEnv/integratesProd"
      ];
      vcpus = 1;
    };
  };
}
