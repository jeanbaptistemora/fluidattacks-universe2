{ inputs
, makeScript
, ...
}:
makeScript {
  replace = {
    __argFirefox__ = inputs.nixpkgs.firefox;
    __argGeckodriver__ = inputs.nixpkgs.geckodriver;
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.kubectl
    ];
    source = [
      inputs.product.integrates-web-e2e-pypi
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "integrates-web-e2e";
  entrypoint = ./entrypoint.sh;
}
