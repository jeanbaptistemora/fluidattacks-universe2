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
      makesVpn = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/makesVpnProd"
          outputs."/secretsForEnvFromSops/makesVpnData"
          outputs."/secretsForTerraformFromEnv/makesVpn"
        ];
        src = "/makes/foss/modules/common/vpn/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      makesVpn = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesVpnDev"
          outputs."/secretsForEnvFromSops/makesVpnData"
          outputs."/secretsForTerraformFromEnv/makesVpn"
        ];
        src = "/makes/foss/modules/common/vpn/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    makesVpnDev = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/makes/secrets/dev.yaml";
    };
    makesVpnProd = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/makes/secrets/prod.yaml";
    };
    makesVpnData = {
      vars = ["VPN_DATA_RAW"];
      manifest = "/makes/secrets/dev.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    makesVpn = {
      cloudflare_api_key = "CLOUDFLARE_API_KEY";
      cloudflare_email = "CLOUDFLARE_EMAIL";
      vpnDataRaw = "VPN_DATA_RAW";
    };
  };
  testTerraform = {
    modules = {
      makesVpn = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/makesVpnDev"
          outputs."/secretsForEnvFromSops/makesVpnData"
          outputs."/secretsForTerraformFromEnv/makesVpn"
        ];
        src = "/makes/foss/modules/common/vpn/infra";
        version = "1.0";
      };
    };
  };
}
