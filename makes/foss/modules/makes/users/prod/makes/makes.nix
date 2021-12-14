# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersProdMakes = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/prod/makes/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersProdMakes = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
        ];
        src = "/makes/foss/modules/makes/users/prod/makes/infra";
        version = "1.0";
      };
    };
  };
  taintTerraform = {
    modules = {
      makesUsersProdMakesKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        resources = [ "module.aws.aws_iam_access_key._1" ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/prod/makes/infra";
        version = "1.0";
      };
      makesUsersProdMakesKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        resources = [ "module.aws.aws_iam_access_key._2" ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/prod/makes/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersProdMakes = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/prod/makes/infra";
        version = "1.0";
      };
    };
  };
}
