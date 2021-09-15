{ inputs
, makeContainerImage
, makeDerivation
, ...
}:
makeContainerImage {
  config.Entrypoint = [ "${inputs.product.skims}/bin/skims" ];
  layers = [
    (makeDerivation {
      builder = ./builder.sh;
      name = "skims-container";
    })
  ];
}
