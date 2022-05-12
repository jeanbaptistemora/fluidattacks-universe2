{outputs, ...}: {
  lintPython = {
    modules = {
      commonOktaCloseSessions = {
        searchPaths.source = [outputs."/common/okta/close-sessions/env"];
        python = "3.9";
        src = "/common/okta/close-sessions/src";
      };
    };
  };
}
