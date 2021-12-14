# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersProdMelts = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/prod/melts/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersProdMelts = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
        ];
        src = "/makes/foss/modules/makes/users/prod/melts/infra";
        version = "1.0";
      };
    };
  };
  taintTerraform = {
    modules = {
      makesUsersProdMeltsKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        resources = [ "module.aws.aws_iam_access_key._1" ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/prod/melts/infra";
        version = "1.0";
      };
      makesUsersProdMeltsKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        resources = [ "module.aws.aws_iam_access_key._2" ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/prod/melts/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersProdMelts = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/prod/melts/infra";
        version = "1.0";
      };
    };
  };
}
