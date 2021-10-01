{ inputs
, makeScript
, ...
}:
makeScript {
  name = "integrates-kill";
  searchPaths.bin = [
    inputs.product.makes-kill-port
  ];
  entrypoint = ./entrypoint.sh;
}
