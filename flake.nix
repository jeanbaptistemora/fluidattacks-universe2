{
  description = "Fluid Attacks, We hack your software!";
  inputs = {
    flake.url = "github:numtide/flake-utils";
    flakeCompat.flake = false;
    flakeCompat.url = "github:edolstra/flake-compat";
    pkgsSrcCommon.url = "github:NixOS/nixpkgs/release-20.03";
    pkgsSrcObserves.url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d";
    pkgsSrcSkims.url = "github:NixOS/nixpkgs/a437fe25652dea5b86de63891ce9c779c6e8bb9d";
    pkgsSrcSkimsTerraform.url = "github:NixOS/nixpkgs/f99908924015bb83df8186b2c473919be35b43f0";
  };
  outputs = attrs: import ./makes attrs;
}
