{ inputs
, makeContainerImage
, makeDerivation
, outputs
, ...
}:
makeContainerImage {
  config.WorkingDir = "/src";
  layers = [
    inputs.nixpkgs.bash
    inputs.nixpkgs.coreutils
    outputs."/forces"
    (makeDerivation {
      builder = ./builder.sh;
      name = "forces-oci-build-customization-layer";
    })
  ];
}
