{ inputs
, ...
}:
{
  lintPython = {
    dirsOfModules = {
      reviews = {
        searchPaths.source = [
          inputs.product.reviews-runtime
        ];
        python = "3.8";
        src = "/reviews/src";
      };
    };
  };
}
