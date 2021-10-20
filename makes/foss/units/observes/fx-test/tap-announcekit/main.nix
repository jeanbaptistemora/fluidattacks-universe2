{ makeScript
, inputs
, projectPath
, ...
}:
makeScript {
  replace = {
    __argEnvSrc__ = projectPath "/observes/singer/tap_announcekit";
    __argEnvTestDir__ = "fx_tests";
  };
  searchPaths = {
    source = [
      inputs.product.observes-generic-tester
      inputs.product.observes-env-tap-announcekit-development
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "observes-fx-test-tap-announcekit";
  entrypoint = ./entrypoint.sh;
}
