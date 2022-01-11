{ inputs
, makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
makeTemplate {
  name = "observes-singer-tap-gitlab-env-runtime";
  searchPaths = {
    pythonPackage = [
      (projectPath inputs.observesIndex.tap.gitlab.root)
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "observes-singer-tap-gitlab-env-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/observes/common/paginator/env/runtime"
      outputs."/observes/common/postgres-client/env/runtime"
      outputs."/observes/common/singer-io/env/runtime"
      outputs."/observes/env/utils-logger/runtime"
    ];
  };
}
