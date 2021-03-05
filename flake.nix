{
  description = "Fluid Attacks, We hack your software!";
  inputs = {
    flakeCompat = { url = "github:edolstra/flake-compat"; flake = false; };

    srcAirsPkgs = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
    srcAssertsPkgs = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
    srcForcesPkgs = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
    srcIntegratesMobilePkgs = { url = "https://github.com/nixos/nixpkgs/archive/932941b79c3dbbef2de9440e1631dfec43956261.tar.gz"; flake = false; };
    srcIntegratesPkgs = { url = "https://github.com/nixos/nixpkgs/archive/932941b79c3dbbef2de9440e1631dfec43956261.tar.gz"; flake = false; };
    srcMakesPkgs = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
    srcMeltsPkgs = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
    srcObservesPkgs = { url = "https://github.com/nixos/nixpkgs/archive/932941b79c3dbbef2de9440e1631dfec43956261.tar.gz"; flake = false; };
    srcReviewsPkgs = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
    srcServesPkgs = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
    srcSkimsPkgs = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
    srcSortsPkgs = { url = "https://github.com/nixos/nixpkgs/archive/7138a338b58713e0dea22ddab6a6785abec7376a.tar.gz"; flake = false; };
  };
  outputs = attrs: import ./makes attrs;
}
