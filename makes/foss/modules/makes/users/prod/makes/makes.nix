# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      makesUsersProdMakes = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/makesUsersProd"
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
          outputs."/secretsForEnvFromSops/makesUsersProd"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        resources = [
          "module.prod_airs_aws.aws_iam_access_key._1"
          "module.prod_docs_aws.aws_iam_access_key._1"
          "module.prod_forces_aws.aws_iam_access_key._1"
          "module.prod_integrates_aws.aws_iam_access_key._1"
          "module.prod_makes_aws.aws_iam_access_key._1"
          "module.prod_melts_aws.aws_iam_access_key._1"
          "module.prod_observes_aws.aws_iam_access_key._1"
          "module.prod_skims_aws.aws_iam_access_key._1"
          "module.prod_sorts_aws.aws_iam_access_key._1"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/prod/makes/infra";
        version = "1.0";
      };
      makesUsersProdMakesKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/makesUsersProd"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        resources = [
          "module.prod_airs_aws.aws_iam_access_key._2"
          "module.prod_docs_aws.aws_iam_access_key._2"
          "module.prod_forces_aws.aws_iam_access_key._2"
          "module.prod_integrates_aws.aws_iam_access_key._2"
          "module.prod_makes_aws.aws_iam_access_key._2"
          "module.prod_melts_aws.aws_iam_access_key._2"
          "module.prod_observes_aws.aws_iam_access_key._2"
          "module.prod_skims_aws.aws_iam_access_key._2"
          "module.prod_sorts_aws.aws_iam_access_key._2"
        ];
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
          outputs."/secretsForEnvFromSops/makesUsersDev"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/prod/makes/infra";
        version = "1.0";
      };
    };
  };
}
