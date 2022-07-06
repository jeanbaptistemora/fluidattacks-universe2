{outputs, ...}: {
  lintPython = {
    modules = {
      integratesJobsCloneRoots = {
        searchPaths.source = [
          outputs."/integrates/jobs/clone_roots/env/pypi"
        ];
        python = "3.9";
        src = "/integrates/jobs/clone_roots/src";
      };
    };
  };
}
