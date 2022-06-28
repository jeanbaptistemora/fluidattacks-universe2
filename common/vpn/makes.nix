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
          outputs."/secretsForAwsFromEnv/prodCommon"
          outputs."/secretsForEnvFromSops/commonCloudflareProd"
          outputs."/secretsForEnvFromSops/commonVpnData"
          outputs."/secretsForTerraformFromEnv/commonVpn"
        ];
        src = "/common/vpn/infra";
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
          outputs."/secretsForEnvFromSops/commonCloudflareDev"
          outputs."/secretsForEnvFromSops/commonVpnData"
          outputs."/secretsForTerraformFromEnv/commonVpn"
        ];
        src = "/common/vpn/infra";
        version = "1.0";
      };
    };
  };
  secretsForEnvFromSops = {
    commonVpnData = {
      vars = ["VPN_DATA_RAW"];
      manifest = "/common/vpn/data.yaml";
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
          outputs."/secretsForEnvFromSops/commonCloudflareDev"
          outputs."/secretsForEnvFromSops/commonVpnData"
          outputs."/secretsForTerraformFromEnv/commonVpn"
        ];
        src = "/common/vpn/infra";
        version = "1.0";
      };
    };
  };
}
