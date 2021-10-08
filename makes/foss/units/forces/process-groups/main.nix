{ makeScript
, inputs
, outputs
, projectPath
, ...
}:
makeScript {
  searchPaths = {
    bin = [
      inputs.nixpkgs.jq
      outputs."/forces"
    ];
    source = [
      inputs.product.melts-lib
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "forces-process-groups";
  entrypoint = projectPath "/makes/foss/units/forces/process-groups/entrypoint.sh";
}
