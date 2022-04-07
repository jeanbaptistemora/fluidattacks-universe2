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
      commonVpn = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/prodMakes"
          outputs."/secretsForEnvFromSops/commonVpnProd"
          outputs."/secretsForEnvFromSops/commonVpnData"
          outputs."/secretsForTerraformFromEnv/commonVpn"
        ];
        src = "/makes/foss/modules/common/vpn/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonVpn = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonVpnDev"
          outputs."/secretsForEnvFromSops/commonVpnData"
          outputs."/secretsForTerraformFromEnv/commonVpn"
        ];
        src = "/makes/foss/modules/common/vpn/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonVpnDev = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/makes/secrets/dev.yaml";
    };
    commonVpnProd = {
      vars = ["CLOUDFLARE_ACCOUNT_ID" "CLOUDFLARE_API_KEY" "CLOUDFLARE_EMAIL"];
      manifest = "/makes/secrets/prod.yaml";
    };
    commonVpnData = {
      vars = ["VPN_DATA_RAW"];
      manifest = "/makes/secrets/dev.yaml";
    };
  };
  secretsForTerraformFromEnv = {
    commonVpn = {
      cloudflare_api_key = "CLOUDFLARE_API_KEY";
      cloudflare_email = "CLOUDFLARE_EMAIL";
      vpnDataRaw = "VPN_DATA_RAW";
    };
  };
  testTerraform = {
    modules = {
      commonVpn = {
        setup = [
          searchPaths
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonVpnDev"
          outputs."/secretsForEnvFromSops/commonVpnData"
          outputs."/secretsForTerraformFromEnv/commonVpn"
        ];
        src = "/makes/foss/modules/common/vpn/infra";
        version = "1.0";
      };
    };
  };
}
