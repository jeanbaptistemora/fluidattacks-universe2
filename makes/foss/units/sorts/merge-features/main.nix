{ makeScript
, inputs
, projectPath
, ...
}:
makeScript {
  name = "sorts-merge-features";
  searchPaths = {
    bin = [ inputs.nixpkgs.python38 ];
    source = [
      inputs.product.sorts-config-development
      inputs.product.sorts-config-runtime
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/sorts/merge-features/entrypoint.sh";
}
