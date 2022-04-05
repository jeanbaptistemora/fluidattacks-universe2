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
      makesVpc = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/makesVpcProd"
          outputs."/secretsForTerraformFromEnv/makesVpc"
        ];
        src = "/makes/foss/modules/makes/vpc/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesVpc = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesVpcDev"
          outputs."/secretsForTerraformFromEnv/makesVpc"
        ];
        src = "/makes/foss/modules/makes/vpc/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    makesVpcDev = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/makes/secrets/dev.yaml";
    };
    makesVpcProd = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/makes/secrets/prod.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesVpc = {
      cloudflare_api_key = "CLOUDFLARE_API_KEY";
      cloudflare_email = "CLOUDFLARE_EMAIL";
    };
  };
  testTerraform = {
    modules = {
      makesVpc = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesVpcDev"
          outputs."/secretsForTerraformFromEnv/makesVpc"
        ];
        src = "/makes/foss/modules/makes/vpc/infra";
        version = "1.0";
      };
    };
  };
}
