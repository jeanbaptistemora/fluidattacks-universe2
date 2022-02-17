# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesUsersProdSorts = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/prod/sorts/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersProdSorts = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/prod/sorts/infra";
        version = "1.0";
      };
    };
  };
  taintTerraform = {
    modules = {
      makesUsersProdSortsKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        resources = [ "module.aws.aws_iam_access_key._1" ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/prod/sorts/infra";
        version = "1.0";
      };
      makesUsersProdSortsKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        resources = [ "module.aws.aws_iam_access_key._2" ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/prod/sorts/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersProdSorts = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/prod/sorts/infra";
        version = "1.0";
      };
    };
  };
}
