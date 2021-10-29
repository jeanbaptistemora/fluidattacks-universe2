{ inputs
, makeScript
, ...
}:
makeScript {
  name = "makes-kill-port";
  searchPaths = {
    bin = [
      inputs.nixpkgs.lsof
    ];
  };
  entrypoint = ./entrypoint.sh;
}
