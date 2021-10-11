{ outputs
, ...
}:
{
  testPython = {
    sorts = {
      python = "3.8";
      searchPaths = {
        source = [
          outputs."/sorts/config-development"
          outputs."/sorts/config-runtime"
        ];
      };
      src = "/sorts/test";
    };
  };
}
