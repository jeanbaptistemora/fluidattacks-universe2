# https://github.com/fluidattacks/makes
{
  imports = [
    ./infra/makes.nix
    ./pipeline/makes.nix
  ];
  secretsForAwsFromEnv = {
    prodAirs = {
      accessKeyId = "PROD_AIRS_AWS_ACCESS_KEY_ID";
      secretAccessKey = "PROD_AIRS_AWS_SECRET_ACCESS_KEY";
    };
  };
  lintMarkdown = {
    airs = {
      config = "/makes/foss/modules/airs/config/markdown.rb";
      targets = [ "/airs/front/content" ];
    };
  };
}
