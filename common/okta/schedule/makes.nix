{outputs, ...}: {
  lintPython = {
    modules = {
      commonOktaScheduleCloseSessions = {
        searchPaths.source = [outputs."/common/okta/schedule/close-sessions/env"];
        python = "3.9";
        src = "/common/okta/schedule/close-sessions/src";
      };
    };
  };
}
