{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  searchPaths = {
    bin = [ inputs.nixpkgs.kubectl ];
    kubeConfig = [ ".kubernetes" ];
    source = [ (outputs."/utils/aws") ];
  };
  name = "integrates-back-destroy-eph";
  entrypoint = ./entrypoint.sh;
}
