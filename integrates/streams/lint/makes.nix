{outputs, ...}: {
  lintPython = {
    dirsOfModules = {
      streams = {
        searchPaths = {
          pythonMypy = [
            outputs."/integrates/streams/runtime"
          ];
          source = [
            outputs."/integrates/streams/runtime"
          ];
        };
        python = "3.11";
        src = "/integrates/streams/src";
      };
    };
  };
}
