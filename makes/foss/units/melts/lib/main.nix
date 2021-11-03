{ inputs
, makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "melts-lib";
  searchPaths = {
    bin = [ outputs."/melts" ];
    source = [
      (outputs."/utils/aws")
      (inputs.legacy.importUtility "git")
    ];
  };
  template = ./template.sh;
}
