# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersForces = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersForces"
        ];
        src = "/makes/makes/users/forces/infra";
        version = "0.13";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersForces = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
        ];
        src = "/makes/makes/users/forces/infra";
        version = "0.13";
      };
    };
  };
  secretsForTerraformFromEnv = {
    makesUsersForces = {
      gitlab_token = "PRODUCT_API_TOKEN";
      region = "AWS_DEFAULT_REGION";
    };
  };
  taintTerraform = {
    modules = {
      makesUsersForcesKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersForces"
        ];
        resources = [
          "aws_iam_access_key.forces_dev_key-1"
          "aws_iam_access_key.forces_prod_key-1"
        ];
        reDeploy = true;
        src = "/makes/makes/users/forces/infra";
        version = "0.13";
      };
      makesUsersForcesKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsersForces"
        ];
        resources = [
          "aws_iam_access_key.forces_dev_key-2"
          "aws_iam_access_key.forces_prod_key-2"
        ];
        reDeploy = true;
        src = "/makes/makes/users/forces/infra";
        version = "0.13";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersForces = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesDev"
          outputs."/secretsForTerraformFromEnv/makesUsersForces"
        ];
        src = "/makes/makes/users/forces/infra";
        version = "0.13";
      };
    };
  };
}
