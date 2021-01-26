let
  src = import ./src/fetch-src.nix {
    repo = "https://github.com/NixOS/nixpkgs";
    commit = "932941b79c3dbbef2de9440e1631dfec43956261";
    digest = "1d4nyjylsvrv9r4ly431wilkswb2pnlfwwg0cagfjch60d4897qp";
  };
in
  import src {
    config.android_sdk.accept_license = true;
  }
