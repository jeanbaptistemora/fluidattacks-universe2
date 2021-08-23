{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "1f535fdedafce35a339ae0ac8baffb8ba3c689db";
  };
}
