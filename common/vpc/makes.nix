# https://github.com/fluidattacks/makes
{
  inputs,
  makeSearchPaths,
  outputs,
  ...
}: let
  searchPaths = makeSearchPaths {
    bin = [inputs.nixpkgs.git];
  };
in {
  deployTerraform = {
    modules = {
      commonVpc = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/prodCommon"
          outputs."/secretsForEnvFromSops/commonVpcProd"
          outputs."/secretsForTerraformFromEnv/commonVpc"
        ];
        src = "/common/vpc/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonVpc = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonVpcDev"
          outputs."/secretsForTerraformFromEnv/commonVpc"
        ];
        src = "/common/vpc/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonVpcDev = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/common/secrets/dev.yaml";
    };
    commonVpcProd = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/common/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    commonVpc = {
      cloudflare_api_key = "CLOUDFLARE_API_KEY";
      cloudflare_email = "CLOUDFLARE_EMAIL";
    };
  };
  testTerraform = {
    modules = {
      commonVpc = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonVpcDev"
          outputs."/secretsForTerraformFromEnv/commonVpc"
        ];
        src = "/common/vpc/infra";
        version = "1.0";
      };
    };
  };
}
