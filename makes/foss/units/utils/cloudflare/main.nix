{ inputs
, makeTemplate
, ...
}:
makeTemplate {
  searchPaths = {
    bin = [
      inputs.nixpkgs.curl
      inputs.nixpkgs.jq
    ];
  };
  name = "utils-cloudflare";
  template = ./template.sh;
}
