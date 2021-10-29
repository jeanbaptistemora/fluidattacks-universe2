{ inputs
, outputs
, makeScript
, ...
}:
makeScript {
  name = "integrates-cache";
  searchPaths = {
    bin = [
      inputs.nixpkgs.redis
      outputs."/makes/done"
      outputs."/makes/kill-port"
      inputs.product.makes-wait
    ];
  };
  entrypoint = ./entrypoint.sh;
}
