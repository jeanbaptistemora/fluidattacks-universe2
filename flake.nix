{
  description = "Fluid Attacks, We hack your software!";
  inputs = {
    flakeCompat = { url = "github:edolstra/flake-compat"; flake = false; };
    srcAirsPkgs = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
    srcAssertsPkgs = { url = "github:Nixos/nixpkgs/f99908924015bb83df8186b2c473919be35b43f0"; flake = false; };
    srcForcesPkgs = { url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d"; flake = false; };
    srcIntegratesMobilePkgs = { url = "github:NixOS/nixpkgs/932941b79c3dbbef2de9440e1631dfec43956261"; flake = false; };
    srcIntegratesPkgs = { url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d"; flake = false; };
    srcMakesPkgs = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
    srcMeltsPkgs = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
    srcObservesPkgs = { url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d"; flake = false; };
    srcReviewsPkgs = { url = "github:NixOS/nixpkgs/f99908924015bb83df8186b2c473919be35b43f0"; flake = false; };
    srcServesPkgs = { url = "github:NixOS/nixpkgs/f99908924015bb83df8186b2c473919be35b43f0"; flake = false; };
    srcSkimsBenchmarkOwaspRepo = { url = "github:OWASP/Benchmark/9a0c25a5f8443245c676965d20d22d5f93da3f99"; flake = false; };
    srcSkimsPkgs = { url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d"; flake = false; };
    srcSkimsTreeSitterRepo = { url = "github:tree-sitter/tree-sitter-java"; flake = false; };
    srcSortsPkgs = { url = "github:NixOS/nixpkgs/5d5e970ce04933576957dfbf99cb7d4c1802c60d"; flake = false; };
  };
  outputs = attrs: import ./makes attrs;
}
