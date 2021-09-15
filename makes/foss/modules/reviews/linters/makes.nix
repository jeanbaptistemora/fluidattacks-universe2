{ inputs
, ...
}:
{
  lintPython = {
    dirsOfModules = {
      reviews = {
        extraSources = [
          inputs.product.reviews-runtime
        ];
        python = "3.8";
        src = "/reviews/src";
      };
    };
  };
}
