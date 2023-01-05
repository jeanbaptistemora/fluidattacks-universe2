{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    ref = "refs/heads/main";
    rev = "7a802fdd918c4d6e8ba6cdccc091079f0b42fd49";
  };
}
