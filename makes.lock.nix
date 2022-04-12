{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    ref = "main";
    rev = "a5ef5225c9fb9723958d7d980c89a7905c658712";
  };
}
