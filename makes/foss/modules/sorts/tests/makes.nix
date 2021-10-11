{ inputs
, ...
}:
{
  testPython = {
    sorts = {
      python = "3.8";
      searchPaths = {
        source = [
          inputs.product.sorts-config-development
          inputs.product.sorts-config-runtime
        ];
      };
      src = "/sorts/test";
    };
  };
}
