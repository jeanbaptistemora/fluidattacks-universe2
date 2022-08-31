# https://github.com/fluidattacks/makes
{
  imports = [
    ./infra/makes.nix
    ./pipeline/makes.nix
  ];
  secretsForAwsFromGitlab = {
    prodAirs = {
      roleArn = "arn:aws:iam::205810638802:role/prod_airs";
      duration = 3600;
    };
  };
  lintMarkdown = {
    airs = {
      config = "/airs/.lint-markdown.rb";
      targets = ["/airs/front/content"];
    };
  };
}
