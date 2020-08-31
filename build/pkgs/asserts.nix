let
  src = import ./src/fetch-src.nix {
    repo = "https://github.com/NixOS/nixpkgs";
    commit = "f99908924015bb83df8186b2c473919be35b43f0";
    digest = "1230z7wwsvrxfwfsdzz825mchdn3n043cz4ky2rgzb93rlihf4r2";
  };
in
  import src { }
