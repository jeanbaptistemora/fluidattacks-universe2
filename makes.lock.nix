{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "0f0ae972efc04a84cd5492d7587287a8294f8fff";
  };
}
