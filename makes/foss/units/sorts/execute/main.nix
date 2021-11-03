{ makeScript
, inputs
, outputs
, projectPath
, ...
}:
makeScript {
  name = "sorts-execute";
  searchPaths = {
    source = [
      outputs."/melts/lib"
      outputs."/sorts/config-runtime"
      (outputs."/utils/aws")
      (inputs.legacy.importUtility "git")
      (inputs.legacy.importUtility "sops")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/sorts/execute/entrypoint.sh";
}
