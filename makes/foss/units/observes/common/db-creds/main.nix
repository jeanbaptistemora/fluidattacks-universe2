{ inputs
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  searchPaths = {
    bin = [
      inputs.nixpkgs.jq
    ];
    source = [
      (outputs."/utils/sops")
    ];
  };
  name = "observes-db-creds";
  template = ./template.sh;
}
