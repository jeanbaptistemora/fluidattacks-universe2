{
  inputs,
  makeScript,
  ...
}:
makeScript {
  name = "docs-generate-graphs";
  aliases = ["generate-graphs"];
  entrypoint = ./entrypoint.sh;
  searchPaths.bin = [
    inputs.nixpkgs.findutils
    inputs.nixpkgs.graphviz
  ];
}
