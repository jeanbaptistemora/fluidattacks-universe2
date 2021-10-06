{ makePythonPypiEnvironment
, ...
}:
makePythonPypiEnvironment {
  name = "integrates-back-unit-tests";
  sourcesYaml = ./pypi-sources.yaml;
  withSetuptools_57_4_0 = true;
  withWheel_0_37_0 = true;
}
