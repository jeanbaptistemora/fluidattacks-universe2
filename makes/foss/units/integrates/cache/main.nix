{ inputs
, makeScript
, managePorts
, ...
}:
makeScript {
  name = "integrates-cache";
  searchPaths = {
    bin = [
      inputs.nixpkgs.redis
    ];
    source = [
      managePorts
    ];
  };
  entrypoint = ./entrypoint.sh;
}
