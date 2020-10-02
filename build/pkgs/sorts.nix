let
  src = import ./src/fetch-src.nix {
    repo = "https://github.com/NixOS/nixpkgs";
    commit = "5b09b92a16f2bafbfcba4fbdfe7084a2b2d97d75";
    digest = "d143d8a8e38556b1e0fea5570c35e2ce81d4eefe0c902e9663d3ebc4d94e27c5";
  };
in
  import src { }
