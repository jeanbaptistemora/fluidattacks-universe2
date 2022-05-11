{outputs, ...}: {
  secretsForEnvFromSops = {
    commonUsersDev = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/common/secrets/dev.yaml";
    };
    commonUsersProd = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/common/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    commonUsers = {
      gitlab_token = "PRODUCT_API_TOKEN";
      gitlab_token_services = "SERVICES_API_TOKEN";
      region = "AWS_DEFAULT_REGION";
    };
  };
  deployTerraform = {
    modules = {
      commonUsers = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodCommon"
          outputs."/secretsForEnvFromSops/commonUsersProd"
          outputs."/secretsForTerraformFromEnv/commonUsers"
        ];
        src = "/common/users/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonUsers = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
        ];
        src = "/common/users/infra";
        version = "1.0";
      };
    };
  };
  taintTerraform = {
    modules = {
      commonUsersKeys1 = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodCommon"
          outputs."/secretsForEnvFromSops/commonUsersProd"
          outputs."/secretsForTerraformFromEnv/commonUsers"
        ];
        resources = [
          "module.dev_aws.aws_iam_access_key._1"
          "module.prod_airs_aws.aws_iam_access_key._1"
          "module.prod_common_aws.aws_iam_access_key._1"
          "module.prod_docs_aws.aws_iam_access_key._1"
          "module.prod_forces_aws.aws_iam_access_key._1"
          "module.prod_integrates_aws.aws_iam_access_key._1"
          "module.prod_melts_aws.aws_iam_access_key._1"
          "module.prod_observes_aws.aws_iam_access_key._1"
          "module.prod_services_aws.aws_iam_access_key._1"
          "module.prod_skims_aws.aws_iam_access_key._1"
          "module.prod_sorts_aws.aws_iam_access_key._1"
        ];
        reDeploy = true;
        src = "/common/users/infra";
        version = "1.0";
      };
      commonUsersKeys2 = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodCommon"
          outputs."/secretsForEnvFromSops/commonUsersProd"
          outputs."/secretsForTerraformFromEnv/commonUsers"
        ];
        resources = [
          "module.dev_aws.aws_iam_access_key._2"
          "module.prod_airs_aws.aws_iam_access_key._2"
          "module.prod_common_aws.aws_iam_access_key._2"
          "module.prod_docs_aws.aws_iam_access_key._2"
          "module.prod_forces_aws.aws_iam_access_key._2"
          "module.prod_integrates_aws.aws_iam_access_key._2"
          "module.prod_melts_aws.aws_iam_access_key._2"
          "module.prod_observes_aws.aws_iam_access_key._2"
          "module.prod_services_aws.aws_iam_access_key._2"
          "module.prod_skims_aws.aws_iam_access_key._2"
          "module.prod_sorts_aws.aws_iam_access_key._2"
        ];
        reDeploy = true;
        src = "/common/users/infra";
        version = "1.0";
      };
    };
  };
  testTerraform = {
    modules = {
      commonUsers = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonUsersDev"
          outputs."/secretsForTerraformFromEnv/commonUsers"
        ];
        src = "/common/users/infra";
        version = "1.0";
      };
    };
  };
}
