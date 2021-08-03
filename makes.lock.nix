{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "8b8fa7ebde4c64666203167c6458a159b5244acd";
  };
}
