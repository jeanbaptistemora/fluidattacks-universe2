{ inputs
, makeTemplate
, ...
}:
makeTemplate {
  name = "melts-lib";
  searchPaths = {
    bin = [ inputs.product.melts ];
    source = [
      (inputs.legacy.importUtility "aws")
      (inputs.legacy.importUtility "git")
    ];
  };
  template = ./template.sh;
}
