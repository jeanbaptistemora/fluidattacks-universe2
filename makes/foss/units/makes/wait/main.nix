{ inputs
, makeScript
, ...
}:
makeScript {
  name = "makes-wait";
  searchPaths = {
    bin = [ inputs.nixpkgs.netcat ];
  };
  entrypoint = ./entrypoint.sh;
}
