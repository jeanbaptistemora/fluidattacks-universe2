{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.nixpkgs.findutils
      inputs.nixpkgs.gawk
      inputs.nixpkgs.kubectl
    ];
    kubeConfig = [".kubernetes"];
    source = [outputs."/common/utils/aws"];
  };
  name = "integrates-back-destroy-eph";
  entrypoint = ./entrypoint.sh;
}
