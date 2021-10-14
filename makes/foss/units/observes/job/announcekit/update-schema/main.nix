{ makeScript
, inputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.product.observes-bin-tap-announcekit
    ];
  };
  name = "observes-job-announcekit-update-schema";
  entrypoint = ./entrypoint.sh;
}
