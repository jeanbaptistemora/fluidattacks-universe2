{ inputs
, ...
}:
{
  lintPython = {
    modules = {
      observesCodeEtl = {
        extraSources = [
          inputs.product.observes-env-code-etl-development
        ];
        python = "3.8";
        src = "/observes/code_etl/code_etl";
      };
      observesCodeEtlTests = {
        extraSources = [
          inputs.product.observes-env-code-etl-development
        ];
        python = "3.8";
        src = "/observes/code_etl/tests";
      };
      observesJobLastSuccess = {
        extraSources = [
          inputs.product.observes-env-job-last-success-runtime
        ];
        python = "3.8";
        src = "/observes/services/job_last_success/job_last_success";
      };
      observesJobLastSuccessTests = {
        extraSources = [
          inputs.product.observes-env-job-last-success-runtime
        ];
        python = "3.8";
        src = "/observes/services/job_last_success/tests";
      };
      observesServiceBatchStability = {
        extraSources = [
          inputs.product.observes-env-service-batch-stability-runtime
        ];
        python = "3.8";
        src = "/observes/services/batch_stability/batch_stability";
      };
    };
  };
}
