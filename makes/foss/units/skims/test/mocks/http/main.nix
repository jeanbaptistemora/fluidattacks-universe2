{ makeScript
, outputs
, ...
}:
makeScript {
  name = "skims-test-mocks-http";
  replace = {
    __argApp__ = ./src;
  };
  entrypoint = ./entrypoint.sh;
  searchPaths.source = [ outputs."/skims/test/mocks/http/env" ];
}
