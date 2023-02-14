{
  src,
  python_version,
  nixpkgs,
  fa-purity,
}:
import src {
  inherit python_version src;
  nixpkgs =
    nixpkgs
    // {
      inherit fa-purity;
    };
}
