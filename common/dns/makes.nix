# https://github.com/fluidattacks/makes
{outputs, ...}: {
  deployTerraform = {
    modules = {
      commonDns = {
        setup = [
          outputs."/secretsForAwsFromEnv/prodCommon"
          outputs."/secretsForEnvFromSops/commonCloudflareProd"
          outputs."/secretsForTerraformFromEnv/commonDns"
        ];
        src = "/common/dns/infra";
        version = "1.0";
      };
    };
  };
  lintTerraform = {
    modules = {
      commonDns = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonCloudflareDev"
          outputs."/secretsForTerraformFromEnv/commonDns"
        ];
        src = "/common/dns/infra";
        version = "1.0";
      };
    };
  };
  secretsForTerraformFromEnv = {
    commonDns = {
      cloudflareApiKey = "CLOUDFLARE_API_KEY";
      cloudflareEmail = "CLOUDFLARE_EMAIL";
    };
  };
  testTerraform = {
    modules = {
      commonDns = {
        setup = [
          outputs."/secretsForAwsFromEnv/dev"
          outputs."/secretsForEnvFromSops/commonCloudflareDev"
          outputs."/secretsForTerraformFromEnv/commonDns"
        ];
        src = "/common/dns/infra";
        version = "1.0";
      };
    };
  };
}
