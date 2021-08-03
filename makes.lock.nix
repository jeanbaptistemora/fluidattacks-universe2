{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "1c0146f26ba87922d933fac6e799740ac6974351";
  };
}
