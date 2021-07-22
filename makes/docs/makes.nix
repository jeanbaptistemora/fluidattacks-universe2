# https://github.com/fluidattacks/makes
{ pathCopy
, ...
}:
{
  imports = [
    ./infra/makes.nix
  ];
  lintMarkdown = {
    docs = {
      config = pathCopy "/makes/docs/style.rb";
      targets = [ "/docs/src/docs" ];
    };
  };
}
