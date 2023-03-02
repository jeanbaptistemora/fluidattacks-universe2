{outputs, ...}: {
  lintPython = {
    modules = {
      commonComputeScheduleTest = {
        python = "3.11";
        src = "/common/compute/schedule/test/src";
        searchPaths.source = [outputs."/common/compute/schedule/test/env"];
      };
    };
  };
}
