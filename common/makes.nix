# https://github.com/fluidattacks/makes
{
  imports = [
    ./ci/makes.nix
    ./compute/makes.nix
    ./cluster/makes.nix
    ./criteria/makes.nix
    ./dns/makes.nix
    ./foss/makes.nix
    ./okta/makes.nix
    ./pipeline/makes.nix
    ./status/makes.nix
    ./users/makes.nix
    ./vpc/makes.nix
    ./vpn/makes.nix
  ];
  secretsForAwsFromEnv = {
    dev = {
      accessKeyId = "DEV_AWS_ACCESS_KEY_ID";
      secretAccessKey = "DEV_AWS_SECRET_ACCESS_KEY";
      sessionToken = "AWS_SESSION_TOKEN";
    };
  };
  secretsForAwsFromGitlab = {
    dev = {
      roleArn = "arn:aws:iam::205810638802:role/dev";
      duration = 3600;
    };
    prodCommon = {
      roleArn = "arn:aws:iam::205810638802:role/prod_common";
      duration = 3600;
    };
  };
  secretsForEnvFromSops = {
    commonCloudflareDev = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_KEY"
        "CLOUDFLARE_EMAIL"
      ];
      manifest = "/common/secrets/dev.yaml";
    };
    commonCloudflareProd = {
      vars = [
        "CLOUDFLARE_ACCOUNT_ID"
        "CLOUDFLARE_API_KEY"
        "CLOUDFLARE_EMAIL"
      ];
      manifest = "/common/secrets/prod.yaml";
    };
  };
}
