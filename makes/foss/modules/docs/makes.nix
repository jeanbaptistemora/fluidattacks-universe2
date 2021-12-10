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
    prodDocs = {
      accessKeyId = "PROD_DOCS_AWS_ACCESS_KEY_ID";
      secretAccessKey = "PROD_DOCS_AWS_SECRET_ACCESS_KEY";
      sessionToken = "AWS_SESSION_TOKEN";
    };
  };
}
