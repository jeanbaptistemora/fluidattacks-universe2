# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      makesUsersProdSkims = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/prod/skims/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsersProdSkims = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
        ];
        src = "/makes/foss/modules/makes/users/prod/skims/infra";
        version = "1.0";
      };
    };
  };
  taintTerraform = {
    modules = {
      makesUsersProdSkimsKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        resources = ["module.aws.aws_iam_access_key._1"];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/prod/skims/infra";
        version = "1.0";
      };
      makesUsersProdSkimsKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        resources = ["module.aws.aws_iam_access_key._2"];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/prod/skims/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsersProdSkims = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/prod/skims/infra";
        version = "1.0";
      };
    };
  };
}
