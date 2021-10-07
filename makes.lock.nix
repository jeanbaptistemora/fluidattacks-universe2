{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "6f2211b3e1b40b8e3daace46d844c0be85b661a5";
  };
}
