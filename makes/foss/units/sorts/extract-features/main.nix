{ makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  name = "sorts-extract-features";
  searchPaths = {
    source = [
      (outputs."/melts/lib")
      (outputs."/sorts/config-runtime")
      (outputs."/utils/aws")
      (outputs."/utils/git")
      (outputs."/utils/sops")
    ];
  };
  entrypoint = projectPath "/makes/foss/units/sorts/extract-features/entrypoint.sh";
}
