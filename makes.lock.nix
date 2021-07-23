{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "0dae5699b8d806e33e18122311c8af9510e18048";
  };
}
