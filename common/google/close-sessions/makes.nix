{outputs, ...}: {
  lintPython = {
    modules = {
      commonGoogleCloseSessions = {
        searchPaths.source = [outputs."/common/google/close-sessions/env"];
        python = "3.9";
        src = "/common/google/close-sessions/src";
      };
    };
  };
}
