{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "4a6ed2304fb8ea457340c874899f2aa060a88b8e";
  };
}
