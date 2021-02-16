{
  description = "Fluid Attacks, We hack your software!";
  inputs = {
    flakeCompat = { url = "github:edolstra/flake-compat"; flake = false; };
    flakeUtils = { url = "github:numtide/flake-utils"; };
    srcForcesPkgs = { url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d"; flake = false; };
    srcForcesPkgsTerraform = { url = "github:NixOS/nixpkgs/f99908924015bb83df8186b2c473919be35b43f0"; };
    srcIntegratesPkgs = { url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d"; flake = false; };
    srcIntegratesPkgsTerraform = { url = "github:NixOS/nixpkgs/f99908924015bb83df8186b2c473919be35b43f0"; flake = false; };
    srcMakesPkgs = { url = "github:NixOS/nixpkgs/7138a338b58713e0dea22ddab6a6785abec7376a"; flake = false; };
    srcMeltsPkgs = { url = "github:NixOS/nixpkgs/7138a338b58713e0dea22ddab6a6785abec7376a"; flake = false; };
    srcObservesPkgs = { url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d"; flake = false; };
    srcObservesPkgsTerraform = { url = "github:NixOS/nixpkgs/f99908924015bb83df8186b2c473919be35b43f0"; flake = false; };
    srcServesPkgs = { url = "github:NixOS/nixpkgs/f99908924015bb83df8186b2c473919be35b43f0"; flake = false; };
    srcSkimsBenchmarkOwaspRepo = { url = "github:OWASP/Benchmark/9a0c25a5f8443245c676965d20d22d5f93da3f99"; flake = false; };
    srcSkimsPkgs = { url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d"; flake = false; };
    srcSkimsPkgsTerraform = { url = "github:NixOS/nixpkgs/f99908924015bb83df8186b2c473919be35b43f0"; flake = false; };
    srcSkimsTreeSitterRepo = { url = "github:tree-sitter/tree-sitter-java"; flake = false; };
    srcSortsPkgs = { url = "github:NixOS/nixpkgs/5d5e970ce04933576957dfbf99cb7d4c1802c60d"; flake = false; };
  };
  outputs = attrs: import ./makes attrs;
}
