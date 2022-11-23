{
  inputs,
  makeScript,
  managePorts,
  outputs,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "opensearch";
  replace = {
    __argOpensearch__ = outputs."/integrates/db/opensearch/pkg";
  };
  searchPaths = {
    bin = [inputs.nixpkgs.jdk11_headless];
    source = [managePorts];
  };
}
