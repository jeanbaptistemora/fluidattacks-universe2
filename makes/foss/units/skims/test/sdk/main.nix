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
    AWS_ACCESS_KEY_ID=$SKIMS_PROD_AWS_ACCESS_KEY_ID \
    AWS_SECRET_ACCESS_KEY=$SKIMS_PROD_AWS_SECRET_ACCESS_KEY \
    python3 __argEntrypoint__
  '';
}
