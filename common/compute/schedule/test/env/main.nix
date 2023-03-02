{makePythonPypiEnvironment, ...}:
makePythonPypiEnvironment {
  name = "common-compute-schedule-env";
  sourcesYaml = ./sources.yaml;
}
