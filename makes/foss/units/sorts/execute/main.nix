{ makeScript
, inputs
, projectPath
, ...
}:
makeScript {
  name = "sorts-execute";
  searchPaths = {
    source = [
      inputs.product.melts-lib
      inputs.product.sorts-config-runtime
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "git")
      (inputs.legacy.importUtility "sops")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/sorts/execute/entrypoint.sh";
}
