{ inputs
, makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  searchPaths = {
    bin = [ inputs.nixpkgs.kubectl ];
    kubeConfig = [ ".kubernetes" ];
    source = [ (outputs."/utils/aws") ];
  };
  name = "integrates-back-destroy-eph";
  entrypoint = projectPath "/makes/foss/units/integrates/back/destroy/eph/entrypoint.sh";
}
