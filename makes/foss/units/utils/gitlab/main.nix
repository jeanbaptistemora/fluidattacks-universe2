{ inputs
, makeTemplate
, ...
}:
makeTemplate {
  name = "utils-gitlab";
  searchPaths = {
    bin = [
      inputs.nixpkgs.curl
      inputs.nixpkgs.jq
    ];
  };
  template = ./template.sh;
}
