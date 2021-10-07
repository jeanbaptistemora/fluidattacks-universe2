{ makeContainerImage
, makeDerivation
, outputs
, ...
}:
makeContainerImage {
  config.Entrypoint = [ "${outputs."/skims"}/bin/skims" ];
  layers = [
    (makeDerivation {
      builder = ./builder.sh;
      name = "skims-container";
    })
  ];
}
