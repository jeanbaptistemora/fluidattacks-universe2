{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "0fb6a5bd41cd85bdfb3a52019f18015ebf15f813";
  };
}
