{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "docs";
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      outputs."/docs"
    ];
  };
  entrypoint = ./entrypoint.sh;
}
