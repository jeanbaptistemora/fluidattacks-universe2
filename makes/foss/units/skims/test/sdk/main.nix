{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  replace = {
    __argEntrypoint__ = ./src/entrypoint.py;
  };
  name = "skims-test-sdk";
  searchPaths = {
    bin = [ inputs.nixpkgs.python38 ];
    source = [ outputs."/skims/config-sdk" ];
  };
  entrypoint = ''
    python3 __argEntrypoint__
  '';
}
