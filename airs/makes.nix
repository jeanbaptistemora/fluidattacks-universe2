# https://github.com/fluidattacks/makes
{
  imports = [
    ./infra/makes.nix
    ./pipeline/makes.nix
  ];
  lintMarkdown = {
    airs = {
      config = "/airs/.lint-markdown.rb";
      targets = ["/airs/front/content"];
    };
  };
}
