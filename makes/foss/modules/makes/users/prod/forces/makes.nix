# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersProdForces = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/prod/forces/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersProdForces = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
        ];
        src = "/makes/foss/modules/makes/users/prod/forces/infra";
        version = "1.0";
      };
    };
  };
  taintTerraform = {
    modules = {
      makesUsersProdForcesKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        resources = [ "module.aws.aws_iam_access_key._1" ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/prod/forces/infra";
        version = "1.0";
      };
      makesUsersProdForcesKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/makesProd"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        resources = [ "module.aws.aws_iam_access_key._2" ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/prod/forces/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersProdForces = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/prod/forces/infra";
        version = "1.0";
      };
    };
  };
}
