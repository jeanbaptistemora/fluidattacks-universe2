{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      observes = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodObserves"
          outputs."/secretsForEnvFromSops/observesProd"
          outputs."/secretsForTerraformFromEnv/observesProd"
        ];
        src = "/makes/foss/modules/observes/infra/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      observes = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/observes/infra/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    observesProd = {
      vars = [ "REDSHIFT_USER" "REDSHIFT_PASSWORD" ];
      manifest = "/observes/secrets-prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    observesProd = {
      clusterUser = "REDSHIFT_USER";
      clusterPass = "REDSHIFT_PASSWORD";
    };
  };
  testTerraform = {
    modules = {
      observes = {
        setup = [ outputs."/secretsForAwsFromEnv/dev" ];
        src = "/makes/foss/modules/observes/infra/infra";
        version = "1.0";
      };
    };
  };
}
