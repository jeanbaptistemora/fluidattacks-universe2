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
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "git")
    ];
  };
  template = ./template.sh;
}
