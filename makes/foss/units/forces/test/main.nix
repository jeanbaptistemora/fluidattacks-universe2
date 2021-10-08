{ makeScript
, inputs
, projectPath
, ...
}:
makeScript {
  name = "forces-test";
  searchPaths = {
    source = [
      inputs.product.forces-config-development
      inputs.product.forces-config-runtime
    ];
  };
  entrypoint = projectPath "/makes/foss/units/forces/test/entrypoint.sh";
}
