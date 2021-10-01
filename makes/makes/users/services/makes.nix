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
        version = "0.14";
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
        version = "0.14";
      };
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersServices = {
      gitlab_token = "PRODUCT_API_TOKEN";
      gitlab_token_services = "SERVICES_API_TOKEN";
      region = "AWS_DEFAULT_REGION";
    };
  };
  taintTerraform = {
    modules = {
      makesUsersServicesKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersServices"
        ];
        resources = [
          "aws_iam_access_key.continuous-dev-key-1"
          "aws_iam_access_key.continuous-prod-key-1"
        ];
        reDeploy = true;
        src = "/makes/makes/users/services/infra";
        version = "0.14";
      };
      makesUsersServicesKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersServices"
        ];
        resources = [
          "aws_iam_access_key.continuous-dev-key-2"
          "aws_iam_access_key.continuous-prod-key-2"
        ];
        reDeploy = true;
        src = "/makes/makes/users/services/infra";
        version = "0.14";
      };
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
        version = "0.14";
      };
    };
  };
}
