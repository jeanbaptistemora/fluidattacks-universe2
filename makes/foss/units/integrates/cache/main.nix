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
      inputs.product.makes-kill-port
      inputs.product.makes-wait
    ];
  };
  entrypoint = ./entrypoint.sh;
}
