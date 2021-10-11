{ outputs
, ...
}:
{
  lintPython = {
    dirsOfModules = {
      sorts = {
        searchPaths.source = [
          outputs."/sorts/config-development"
          outputs."/sorts/config-runtime"
        ];
        python = "3.8";
        src = "/sorts/sorts";
      };
    };
    imports = {
      sorts = {
        config = "/sorts/setup.imports.cfg";
        src = "/sorts/sorts";
      };
    };
    modules = {
      sortsTests = {
        searchPaths.source = [
          outputs."/sorts/config-development"
          outputs."/sorts/config-runtime"
        ];
        python = "3.8";
        src = "/sorts/test";
      };
      sortsTraining = {
        searchPaths.source = [
          outputs."/sorts/config-development"
          outputs."/sorts/config-runtime"
        ];
        python = "3.8";
        src = "/sorts/training";
      };
    };
  };
}
