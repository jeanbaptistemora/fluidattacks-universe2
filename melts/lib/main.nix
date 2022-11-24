{
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  name = "melts-lib";
  searchPaths = {
    bin = [outputs."/melts"];
    source = [outputs."/common/utils/git"];
  };
  template = ./template.sh;
}
