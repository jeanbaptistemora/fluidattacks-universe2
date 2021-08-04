{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "34f5a5b1bbf77494e988490867d27a1f65bf36c2";
  };
}
