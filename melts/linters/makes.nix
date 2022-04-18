{outputs, ...}: {
  lintPython = {
    modules = {
      melts = {
        searchPaths.source = [
          outputs."/melts/config/development"
          outputs."/melts/config/runtime"
        ];
        python = "3.8";
        src = "/melts/toolbox";
      };
      meltsTest = {
        searchPaths.source = [
          outputs."/melts/config/development"
          outputs."/melts/config/runtime"
        ];
        python = "3.8";
        src = "/melts/test/src";
      };
    };
  };
}
