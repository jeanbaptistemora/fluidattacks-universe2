{ inputs
, makeTemplate
, ...
}:
makeTemplate {
  name = "utils-env";
  searchPaths = {
    bin = [
      inputs.nixpkgs.curl
      inputs.nixpkgs.jq
    ];
    source = [
      (inputs.legacy.importUtility "gitlab")
    ];
  };
  template = ./template.sh;
}
