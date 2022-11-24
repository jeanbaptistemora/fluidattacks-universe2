{outputs, ...}: {
  lintPython = {
    dirsOfModules = {
      reviews = {
        searchPaths.source = [
          outputs."/reviews/runtime"
        ];
        python = "3.9";
        src = "/reviews/src";
      };
    };
  };
}
