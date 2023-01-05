{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    ref = "refs/heads/main";
    rev = "bd2848c799aac0f04e211f16547dad41c6e3190e";
  };
}
