# https://github.com/fluidattacks/makes
{ projectPath
, ...
}:
{
  imports = [
    ./infra/makes.nix
  ];
  lintMarkdown = {
    docs = {
      config = projectPath "/makes/docs/config/markdown.rb";
      targets = [ "/docs/src/docs" ];
    };
  };
}
