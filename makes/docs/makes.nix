# https://github.com/fluidattacks/makes
{ pathCopy
, ...
}:
{
  lintMarkdown = {
    docs = {
      config = pathCopy "/makes/docs/style.rb";
      targets = [ "/docs/src/docs" ];
    };
  };
}
