{ makeScript
, inputs
, projectPath
, ...
}:
makeScript {
  name = "sorts-extract-features";
  searchPaths = {
    source = [
      inputs.product.melts-lib
      inputs.product.sorts-config-runtime
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "git")
      (inputs.legacy.importUtility "sops")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/sorts/extract-features/entrypoint.sh";
}
