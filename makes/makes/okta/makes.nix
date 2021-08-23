# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesOkta = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/makes/okta/parse"
          outputs."/secretsForEnvFromSops/makesOktaApiToken"
          outputs."/secretsForTerraformFromEnv/makesOkta"
        ];
        src = "/makes/makes/okta/src/infra";
        version = "0.14";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesOkta = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/makes/okta/parse"
          outputs."/secretsForEnvFromSops/makesOktaApiToken"
          outputs."/secretsForTerraformFromEnv/makesOkta"
        ];
        src = "/makes/makes/okta/src/infra";
        version = "0.14";
      };
    };
  };
  secretsForEnvFromSops = {
    makesOktaData = {
      vars = [ "OKTA_DATA_RAW" ];
      manifest = "/makes/makes/okta/src/data.yaml";
    };
    makesOktaApiToken = {
      vars = [ "OKTA_API_TOKEN" ];
      manifest = "/makes/makes/okta/src/data.yaml";
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
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/makes/okta/parse"
          outputs."/secretsForEnvFromSops/makesOktaApiToken"
          outputs."/secretsForTerraformFromEnv/makesOkta"
        ];
        src = "/makes/makes/okta/src/infra";
        version = "0.14";
      };
    };
  };
}
