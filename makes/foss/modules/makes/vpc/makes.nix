# https://github.com/fluidattacks/makes
{ outputs
, ...
}:
{
  deployTerraform = {
    modules = {
      makesVpc = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/makesVpcProd"
          outputs."/secretsForEnvFromSops/makesVpcVpnData"
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
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesVpcDev"
          outputs."/secretsForEnvFromSops/makesVpcVpnData"
          outputs."/secretsForTerraformFromEnv/makesVpc"
        ];
        src = "/makes/foss/modules/makes/vpc/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    makesVpcDev = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/foss/modules/makes/secrets/dev.yaml";
    };
    makesVpcProd = {
      vars = [ "CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL" ];
      manifest = "/makes/foss/modules/makes/secrets/prod.yaml";
    };
    makesVpcVpnData = {
      vars = [ "VPN_DATA_RAW" ];
      manifest = "/makes/foss/modules/makes/secrets/dev.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesVpc = {
      cloudflare_api_key = "CLOUDFLARE_API_KEY";
      cloudflare_email = "CLOUDFLARE_EMAIL";
      vpnDataRaw = "VPN_DATA_RAW";
    };
  };
  testTerraform = {
    modules = {
      makesVpc = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesVpcDev"
          outputs."/secretsForEnvFromSops/makesVpcVpnData"
          outputs."/secretsForTerraformFromEnv/makesVpc"
        ];
        src = "/makes/foss/modules/makes/vpc/infra";
        version = "1.0";
      };
    };
  };
}
