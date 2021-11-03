{ inputs
, makeScript
, outputs
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
      outputs."/integrates/web/e2e/pypi"
      (outputs."/utils/aws")
      (inputs.legacy.importUtility "sops")
    ];
  };
  name = "integrates-web-e2e";
  entrypoint = ./entrypoint.sh;
}
