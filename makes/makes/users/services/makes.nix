# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersServices = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersServices"
        ];
        src = "/makes/makes/users/services/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersServices = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForTerraformFromEnv/makesUsersServices"
        ];
        src = "/makes/makes/users/services/infra";
        version = "0.13";
      };
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersServices = {
      gitlab_token = "PRODUCT_API_TOKEN";
      gitlab_token_services = "SERVICES_API_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      makesUsersServices = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForTerraformFromEnv/makesUsersServices"
        ];
        src = "/makes/makes/users/services/infra";
        version = "0.13";
      };
    };
  };
}
