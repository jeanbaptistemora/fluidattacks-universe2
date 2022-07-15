{outputs, ...}: {
  lintPython = {
    modules = {
      skimsServersReport = {
        searchPaths = {
          source = [
            outputs."/skims/servers/report/env"
          ];
        };
        python = "3.9";
        src = "/skims/servers/report/server";
      };
    };
  };
}
