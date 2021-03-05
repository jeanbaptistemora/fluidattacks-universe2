{
  description = "Fluid Attacks, We hack your software!";
  inputs = {
    flakeCompat = { url = "github:edolstra/flake-compat"; flake = false; };
    nixpkgsSource = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
    nixpkgsSource2 = { url = "https://github.com/nixos/nixpkgs/archive/932941b79c3dbbef2de9440e1631dfec43956261.tar.gz"; flake = false; };
  };
  outputs = attrs: import ./makes attrs;
}
