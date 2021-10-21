# https://github.com/fluidattacks/makes
{
  imports = [
    ./infra/makes.nix
  ];
  lintMarkdown = {
    docs = {
      config = "/makes/foss/modules/docs/config/markdown.rb";
      targets = [ "/docs/src/docs" ];
    };
  };
  secretsForAwsFromEnv = {
    docsProd = {
      accessKeyId = "DOCS_PROD_AWS_ACCESS_KEY_ID";
      secretAccessKey = "DOCS_PROD_AWS_SECRET_ACCESS_KEY";
    };
  };
}
