{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/services/timedoctor_tokens";
in
makeTemplate {
  name = "observes-env-service-timedoctor-tokens-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      packages.observes.bin.update-project-variable
      service-timedoctor-tokens.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      service-timedoctor-tokens.runtime.python
    ];
  };
}
