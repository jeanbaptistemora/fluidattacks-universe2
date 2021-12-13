# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesOkta = {
        setup = [
          outputs."/makes/okta/parse"
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/makesOktaApiToken"
          outputs."/secretsForTerraformFromEnv/makesOkta"
        ];
        src = "/makes/foss/modules/makes/okta/src/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesOkta = {
        setup = [
          outputs."/makes/okta/parse"
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesOktaApiToken"
          outputs."/secretsForTerraformFromEnv/makesOkta"
        ];
        src = "/makes/foss/modules/makes/okta/src/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    makesOktaData = {
      vars = [ "OKTA_DATA_RAW" ];
      manifest = "/makes/foss/modules/makes/okta/src/data.yaml";
    };
    makesOktaApiToken = {
      vars = [ "OKTA_API_TOKEN" ];
      manifest = "/makes/foss/modules/makes/okta/src/data.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesOkta = {
      oktaApiToken = "OKTA_API_TOKEN";
      oktaData = "OKTA_DATA";
    };
  };
  testTerraform = {
    modules = {
      makesOkta = {
        setup = [
          outputs."/makes/okta/parse"
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesOktaApiToken"
          outputs."/secretsForTerraformFromEnv/makesOkta"
        ];
        src = "/makes/foss/modules/makes/okta/src/infra";
        version = "1.0";
      };
    };
  };
}
