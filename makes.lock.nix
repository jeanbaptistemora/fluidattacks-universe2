{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "3159fe0ab88b9a26a268c443c71de68725a93415";
  };
}
