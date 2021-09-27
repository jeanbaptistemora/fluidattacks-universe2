{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "6f13bbdc1ee6779a44eaa1d52f47ab333aa491d6";
  };
}
