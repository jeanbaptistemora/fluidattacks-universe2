{ inputs
, makeContainerImage
, makeDerivation
, ...
}:
makeContainerImage {
  config.WorkingDir = "/src";
  layers = [
    inputs.nixpkgs.bash
    inputs.nixpkgs.coreutils
    inputs.product.forces
    (makeDerivation {
      builder = ./builder.sh;
      name = "forces-oci-build-customization-layer";
    })
  ];
}
