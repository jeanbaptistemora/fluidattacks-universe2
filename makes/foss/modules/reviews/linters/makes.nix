{ outputs
, ...
}:
{
  lintPython = {
    dirsOfModules = {
      reviews = {
        searchPaths.source = [
          outputs."/reviews/runtime"
        ];
        python = "3.8";
        src = "/reviews/src";
      };
    };
  };
}
