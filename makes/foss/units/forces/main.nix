{ inputs
, makeScript
, ...
}:
makeScript {
  name = "forces";
  searchPaths = {
    source = [ inputs.product.forces-config-runtime ];
  };
  entrypoint = ./entrypoint.sh;
}
