{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "c09d7491cbc1fb52793e20f7c73e0def5f0b62aa";
  };
}
