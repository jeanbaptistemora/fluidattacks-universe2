{ nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = path "/makes/applications/skims/test/sdk/src/entrypoint.py";
  };
  name = "skims-test-sdk";
  searchPaths = {
    envSources = [ packages.skims.config-sdk ];
    envPaths = [ nixpkgs.python38 ];
  };
  template = ''
    python3 __envEntrypoint__
  '';
}
