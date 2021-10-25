{ makeScript
, inputs
, ...
}:
makeScript {
  name = "melts";
  searchPaths = {
    source = [ inputs.product.melts-config-runtime ];
  };
  entrypoint = ./entrypoint.sh;
}
