# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      commonSchedule = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodCommon"
          outputs."/secretsForTerraformFromEnv/commonSchedule"
        ];
        src = "/common/schedule/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonSchedule = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForTerraformFromEnv/commonSchedule"
        ];
        src = "/common/schedule/infra";
        version = "1.0";
      };
    };
  };
  secretsForTerraformFromEnv = {
    commonSchedule = {
      productApiToken = "PRODUCT_API_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      commonSchedule = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForTerraformFromEnv/commonSchedule"
        ];
        src = "/common/schedule/infra";
        version = "1.0";
      };
    };
  };
}
