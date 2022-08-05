{outputs, ...}: {
  deployTerraform = {
    modules = {
      observes = {
        setup = [
          outputs."/secretsForEnvFromSops/observesProd"
          outputs."/secretsForTerraformFromEnv/observesProd"
        ];
        src = "/observes/infra/src";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      observes = {
        src = "/observes/infra/src";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    observesProd = {
      vars = ["REDSHIFT_USER" "REDSHIFT_PASSWORD"];
      manifest = "/observes/secrets/prod.yaml";
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
        src = "/observes/infra/src";
        version = "1.0";
      };
    };
  };
}
