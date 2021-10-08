{ makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  name = "forces-test";
  searchPaths = {
    source = [
      outputs."/forces/config-development"
      outputs."/forces/config-runtime"
    ];
  };
  entrypoint = projectPath "/makes/foss/units/forces/test/entrypoint.sh";
}
