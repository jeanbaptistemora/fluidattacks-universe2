{ makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  name = "sorts-execute";
  searchPaths = {
    source = [
      (outputs."/melts/lib")
      (outputs."/sorts/config-runtime")
      (outputs."/utils/aws")
      (outputs."/utils/git")
      (outputs."/utils/sops")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/sorts/execute/entrypoint.sh";
}
