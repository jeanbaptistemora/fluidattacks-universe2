{
  description = "Fluid Attacks, We hack your software!";
  inputs = {
    flake.url = "github:numtide/flake-utils";
    flakeCompat.flake = false;
    flakeCompat.url = "github:edolstra/flake-compat";
    srcIntegratesPkgs.url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d";
    srcMakesPkgs.url = "github:NixOS/nixpkgs/7138a338b58713e0dea22ddab6a6785abec7376a";
    srcMeltsPkgs.url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d";
    srcObservesPkgs.url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d";
    srcSkimsBenchmarkOwaspRepo.flake = false;
    srcSkimsBenchmarkOwaspRepo.url = "github:OWASP/Benchmark/9a0c25a5f8443245c676965d20d22d5f93da3f99";
    srcSkimsPkgs.url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d";
    srcSkimsPkgsTerraform.url = "github:NixOS/nixpkgs/f99908924015bb83df8186b2c473919be35b43f0";
    srcSkimsTreeSitterRepo.flake = false;
    srcSkimsTreeSitterRepo.url = "github:tree-sitter/tree-sitter-java/f7b62ac33d63bea56ce202ace107aaa4285e50af";
    srcSortsPkgs.url = "github:NixOS/nixpkgs/5d5e970ce04933576957dfbf99cb7d4c1802c60d";
  };
  outputs = attrs: import ./makes attrs;
}
