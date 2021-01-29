{ observesPkgs }:
{
  codeEtl = {
    binName = "observes-code-etl";
    entrypoint = "from code_etl.cli import main";
    package = observesPkgs.codeEtl;
  };
}
