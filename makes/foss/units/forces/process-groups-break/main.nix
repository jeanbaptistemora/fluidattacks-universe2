{ makeScript
, inputs
, projectPath
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.nixpkgs.jq
      inputs.product.forces
    ];
    source = [
      inputs.product.melts.lib
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "forces-process-groups-break";
  entrypoint = projectPath "/makes/foss/units/forces/process-groups-break/entrypoint.sh";
}
