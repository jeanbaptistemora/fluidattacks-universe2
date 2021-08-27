# https://github.com/fluidattacks/makes
{
  imports = [
    ./infra/makes.nix
  ];
  lintMarkdown = {
    docs = {
      config = "/makes/docs/config/markdown.rb";
      targets = [ "/docs/src/docs" ];
    };
  };
}
