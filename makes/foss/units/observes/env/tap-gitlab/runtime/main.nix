{ makePythonPypiEnvironment
, makeTemplate
, inputs
, outputs
, projectPath
, ...
}:
makeTemplate {
  name = "observes-env-tap-gitlab-runtime";
  searchPaths = {
    pythonPackage = [
      (projectPath "/observes/singer/tap_gitlab")
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-env-tap-gitlab-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/paginator/runtime"
      inputs.product.observes-env-postgres-client-runtime
      inputs.product.observes-env-singer-io-runtime
      inputs.product.observes-env-utils-logger-runtime
    ];
  };
}
