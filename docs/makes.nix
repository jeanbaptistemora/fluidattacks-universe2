# https://github.com/fluidattacks/makes
{
  imports = [
    ./infra/makes.nix
  ];
  dev.docs = {};
  lintMarkdown = {
    docs = {
      config = "/docs/.lint-markdown.rb";
      targets = ["/docs/src/docs"];
    };
  };
  secretsForAwsFromGitlab = {
    prodDocs = {
      roleArn = "arn:aws:iam::205810638802:role/prod_docs";
      duration = 3600;
    };
  };
}
