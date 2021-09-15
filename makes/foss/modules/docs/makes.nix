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
}
