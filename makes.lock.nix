{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "8dc3af7b2aae60dac3787b526393650d168d2caa";
  };
}
