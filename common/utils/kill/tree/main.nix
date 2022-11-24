{
  inputs,
  makeScript,
  ...
}:
makeScript {
  name = "common-kill-tree";
  searchPaths = {
    bin = [
      inputs.nixpkgs.procps
    ];
  };
  entrypoint = ./entrypoint.sh;
}
