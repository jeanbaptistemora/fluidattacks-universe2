{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    ref = "main";
    rev = "3ae55ac2dfe5f1b990b23240cece179ab1a96305";
  };
}
