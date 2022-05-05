# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      commonCompute = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodCommon"
          outputs."/secretsForTerraformFromEnv/commonCompute"
        ];
        src = "/common/compute/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonCompute = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForTerraformFromEnv/commonCompute"
        ];
        src = "/common/compute/infra";
        version = "1.0";
      };
    };
  };
  secretsForTerraformFromEnv = {
    commonCompute = {
      productApiToken = "PRODUCT_API_TOKEN";
    };
  };
  testTerraform = {
    modules = {
      commonCompute = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForTerraformFromEnv/commonCompute"
        ];
        src = "/common/compute/infra";
        version = "1.0";
      };
    };
  };
}
