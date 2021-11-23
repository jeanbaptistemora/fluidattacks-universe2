{ makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
makeTemplate {
  name = "observes-singer-tap-gitlab-env-runtime";
  searchPaths = {
    pythonPackage = [
      (projectPath "/observes/singer/tap_gitlab")
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-gitlab-env-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/env/paginator/runtime"
      outputs."/observes/env/postgres-client/runtime"
      outputs."/observes/env/singer-io/runtime"
      outputs."/observes/env/utils-logger/runtime"
    ];
  };
}
