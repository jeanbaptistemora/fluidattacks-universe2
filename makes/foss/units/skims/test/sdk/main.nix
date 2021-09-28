{ inputs
, makeScript
, ...
}:
makeScript {
  replace = {
    __argEntrypoint__ = ./src/entrypoint.py;
  };
  name = "skims-test-sdk";
  searchPaths = {
    bin = [ inputs.nixpkgs.python38 ];
    source = [ inputs.product.skims-config-sdk ];
  };
  entrypoint = ''
    set -x
    python3 __argEntrypoint__
  '';
}
