{
  inputs,
  makeTemplate,
  projectPath,
  ...
}:
makeTemplate {
  replace = {
    __argParser__ = projectPath "/common/okta/src/parser/__init__.py";
    __argSopsData__ = projectPath "/common/okta/src/data.yaml";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.python39
      inputs.nixpkgs.sops
    ];
  };
  template = ./template.sh;
  name = "okta-parse";
}
