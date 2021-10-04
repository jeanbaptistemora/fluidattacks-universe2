{ inputs
, makeScript
, projectPath
, ...
}:
makeScript {
  searchPaths = {
    bin = [ inputs.nixpkgs.kubectl ];
    kubeConfig = [ ".kubernetes" ];
    source = [ (inputs.legacy.importUtility "aws") ];
  };
  name = "integrates-back-destroy-eph";
  entrypoint = projectPath "/makes/foss/units/integrates/back/destroy/eph/entrypoint.sh";
}
