# https://github.com/fluidattacks/makes
{
  imports = [
    ./infra/makes.nix
  ];
  lintMarkdown = {
    docs = {
      config = "/docs/.lint-markdown.rb";
      targets = ["/docs/src/docs"];
    };
  };
}
