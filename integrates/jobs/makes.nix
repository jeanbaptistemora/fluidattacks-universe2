{outputs, ...}: {
  lintPython = {
    modules = {
      integratesJobsCloneRoots = {
        searchPaths = {
          source = [
            outputs."/integrates/jobs/clone_roots/env"
          ];
        };
        python = "3.11";
        src = "/integrates/jobs/clone_roots/src";
      };
      integratesJobsExecuteMachine = {
        searchPaths = {
          source = [
            outputs."/integrates/jobs/execute_machine/env"
          ];
        };
        python = "3.11";
        src = "/integrates/jobs/execute_machine/src";
      };
    };
  };
}
