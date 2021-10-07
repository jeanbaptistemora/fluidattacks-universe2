{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "2294eaf16b23f6d777648bc01d04b4e1ac527034";
  };
}
