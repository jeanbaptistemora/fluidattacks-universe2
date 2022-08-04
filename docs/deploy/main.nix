{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "docs-deploy";
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      outputs."/docs"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
