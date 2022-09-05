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
    source = [
      outputs."/common/utils/aws"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
