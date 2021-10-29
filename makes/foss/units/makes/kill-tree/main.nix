{ inputs
, makeScript
, ...
}:
makeScript {
  name = "makes-kill-tree";
  searchPaths = {
    bin = [
      inputs.nixpkgs.procps
    ];
  };
  entrypoint = ./entrypoint.sh;
}
