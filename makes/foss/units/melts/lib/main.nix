{ makeTemplate
, outputs
, ...
}:
makeTemplate {
  name = "melts-lib";
  searchPaths = {
    bin = [ outputs."/melts" ];
    source = [
      outputs."/utils/aws"
      outputs."/utils/git"
    ];
  };
  template = ./template.sh;
}
