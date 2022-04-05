{outputs, ...}: {
  imports = [
    ./infra_roles/makes.nix
  ];
  secretsForEnvFromSops = {
    makesUsersDev = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/makes/secrets/dev.yaml";
    };
    makesUsersProd = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/makes/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesUsers = {
      gitlab_token = "PRODUCT_API_TOKEN";
      gitlab_token_services = "SERVICES_API_TOKEN";
      region = "AWS_DEFAULT_REGION";
    };
  };
  deployTerraform = {
    modules = {
      makesUsers = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/makesUsersProd"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesUsers = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
        ];
        src = "/makes/foss/modules/makes/users/infra";
        version = "1.0";
      };
    };
  };
  taintTerraform = {
    modules = {
      makesUsersKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/makesUsersProd"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        resources = [
          "module.dev_aws.aws_iam_access_key._1"
          "module.prod_airs_aws.aws_iam_access_key._1"
          "module.prod_docs_aws.aws_iam_access_key._1"
          "module.prod_forces_aws.aws_iam_access_key._1"
          "module.prod_integrates_aws.aws_iam_access_key._1"
          "module.prod_makes_aws.aws_iam_access_key._1"
          "module.prod_melts_aws.aws_iam_access_key._1"
          "module.prod_observes_aws.aws_iam_access_key._1"
          "module.prod_services_aws.aws_iam_access_key._1"
          "module.prod_skims_aws.aws_iam_access_key._1"
          "module.prod_sorts_aws.aws_iam_access_key._1"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/infra";
        version = "1.0";
      };
      makesUsersKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/makesUsersProd"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        resources = [
          "module.dev_aws.aws_iam_access_key._2"
          "module.prod_airs_aws.aws_iam_access_key._2"
          "module.prod_docs_aws.aws_iam_access_key._2"
          "module.prod_forces_aws.aws_iam_access_key._2"
          "module.prod_integrates_aws.aws_iam_access_key._2"
          "module.prod_makes_aws.aws_iam_access_key._2"
          "module.prod_melts_aws.aws_iam_access_key._2"
          "module.prod_observes_aws.aws_iam_access_key._2"
          "module.prod_services_aws.aws_iam_access_key._2"
          "module.prod_skims_aws.aws_iam_access_key._2"
          "module.prod_sorts_aws.aws_iam_access_key._2"
        ];
        reDeploy = true;
        src = "/makes/foss/modules/makes/users/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      makesUsers = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesUsersDev"
          outputs."/secretsForTerraformFromEnv/makesUsers"
        ];
        src = "/makes/foss/modules/makes/users/infra";
        version = "1.0";
      };
    };
  };
}
