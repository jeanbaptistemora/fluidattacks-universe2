{
  outputs,
  projectPath,
  ...
}: {
  lintPython = {
    modules = {
      integratesJobsCloneRoots = {
        searchPaths = {
          source = [
            outputs."/integrates/jobs/clone_roots/env"
          ];
          pythonMypy = [
            (projectPath "/integrates/jobs/clone_roots/src")
          ];
        };
        python = "3.8";
        src = "/integrates/jobs/clone_roots/src";
      };
    };
  };
}
