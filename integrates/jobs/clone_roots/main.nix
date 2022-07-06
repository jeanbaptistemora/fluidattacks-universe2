{
  makeScript,
  makePythonVersion,
  outputs,
  ...
}:
makeScript {
  name = "integrates-jobs-clone-roots";
  replace = {
    __argPythonEnv__ = outputs."/integrates/jobs/clone_roots/env/pypi";
    __argScript__ = ./src/__init__.py;
  };
  searchPaths = {
    bin = [(makePythonVersion "3.8")];
  };
  entrypoint = ./entrypoint.sh;
}
