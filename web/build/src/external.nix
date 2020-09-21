pkgs:

rec {
  srcExternalSops = pkgs.fetchurl {
    url = "https://gitlab.com/fluidattacks/public/-/raw/3f902492/shared-scripts/sops.sh";
    sha256 = "0alm1k5dj5fvcdyygm9bk58kgpkjnzl2k7p7d5if5cw8j8bi32rb";
  };
}
