# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersSorts = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersSorts"
        ];
        src = "/makes/makes/users/sorts/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersSorts = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForTerraformFromEnv/makesUsersSorts"
        ];
        src = "/makes/makes/users/sorts/infra";
        version = "0.13";
      };
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersSorts = {
      gitlab_token = "PRODUCT_API_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      makesUsersSorts = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForTerraformFromEnv/makesUsersSorts"
        ];
        src = "/makes/makes/users/sorts/infra";
        version = "0.13";
      };
    };
  };
}
