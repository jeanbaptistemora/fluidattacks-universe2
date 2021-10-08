{ makeScript
, inputs
, projectPath
, ...
}:
makeScript {
  name = "melts-test";
  searchPaths = {
    source = [
      inputs.product.melts-config-development
      inputs.product.melts-config-runtime
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "git")
    ];
    bin = [
      inputs.nixpkgs.gnugrep
    ];
  };
  entrypoint = projectPath "/makes/foss/units/melts/test/entrypoint.sh";
}
