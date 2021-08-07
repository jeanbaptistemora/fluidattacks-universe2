{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "fb178da4c1c62f9e7cce322576787a5ce13f52b7";
  };
}
