{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "10ee5d02562c7984559e8fe9215bb85463f38ca0";
  };
}
