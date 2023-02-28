let
  imports = builtins.foldl' (x: y: x // (import y)) {};
in
  imports [
    ./schedules.nix
  ]
