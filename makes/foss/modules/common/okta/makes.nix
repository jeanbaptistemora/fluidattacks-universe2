# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      commonOkta = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/common/okta/parse"
          outputs."/secretsForEnvFromSops/commonOktaApiToken"
          outputs."/secretsForTerraformFromEnv/commonOkta"
        ];
        src = "/makes/foss/modules/common/okta/src/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonOkta = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/common/okta/parse"
          outputs."/secretsForEnvFromSops/commonOktaApiToken"
          outputs."/secretsForTerraformFromEnv/commonOkta"
        ];
        src = "/makes/foss/modules/common/okta/src/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonOktaData = {
      vars = ["OKTA_DATA_RAW"];
      manifest = "/makes/foss/modules/common/okta/src/data.yaml";
    };
    commonOktaApiToken = {
      vars = ["OKTA_API_TOKEN"];
      manifest = "/makes/foss/modules/common/okta/src/data.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    commonOkta = {
      oktaApiToken = "OKTA_API_TOKEN";
      oktaData = "OKTA_DATA";
    };
  };
  testTerraform = {
    modules = {
      commonOkta = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/common/okta/parse"
          outputs."/secretsForEnvFromSops/commonOktaApiToken"
          outputs."/secretsForTerraformFromEnv/commonOkta"
        ];
        src = "/makes/foss/modules/common/okta/src/infra";
        version = "1.0";
      };
    };
  };
}
