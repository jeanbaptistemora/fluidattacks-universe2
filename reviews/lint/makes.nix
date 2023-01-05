{outputs, ...}: {
  lintPython = {
    dirsOfModules = {
      reviews = {
        searchPaths.source = [
          outputs."/reviews/runtime"
        ];
        python = "3.11";
        src = "/reviews/src";
      };
    };
  };
}
