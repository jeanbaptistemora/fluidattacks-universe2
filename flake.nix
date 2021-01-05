{
  description = "Fluid Attacks, We hack your software!";
  inputs = {
    flake.url = "github:numtide/flake-utils";
    flakeCompat.flake = false;
    flakeCompat.url = "github:edolstra/flake-compat";
    srcCommonPkgsNixLinter.flake = false;
    srcCommonPkgsNixLinter.url = "github:Synthetica9/nix-linter";
    srcCommonPkgsNixLinterPkgs.url = "github:NixOS/nixpkgs/72b9660dc18ba347f7cd41a9504fc181a6d87dc3";
    srcCommonPkgs.url = "github:NixOS/nixpkgs/release-20.03";
    srcMeltsPkgs.url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d";
    srcObservesPkgs.url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d";
    srcSkimsPkgs.url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d";
    srcSkimsPkgsTerraform.url = "github:NixOS/nixpkgs/f99908924015bb83df8186b2c473919be35b43f0";
    srcSkimsBenchmarkOwaspRepo.flake = false;
    srcSkimsBenchmarkOwaspRepo.url = "github:OWASP/Benchmark/9a0c25a5f8443245c676965d20d22d5f93da3f99";
  };
  outputs = attrs: import ./makes attrs;
}
