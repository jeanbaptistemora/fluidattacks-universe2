let
  src = import ./src/fetch-src.nix {
    repo = "https://github.com/NixOS/nixpkgs";
    commit = "a437fe25652dea5b86de63891ce9c779c6e8bb9d";
    digest = "1qqrglpgld1rdasf2018mmzd5cr2vf16mf519q04mc7v3fwfhgws";
  };
in
  import src {
    config.android_sdk.accept_license = true;
  }
