{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    ref = "refs/heads/main";
    rev = "92a5b83d4da409e3052de8dc90be072f94bfce43";
  };
}
