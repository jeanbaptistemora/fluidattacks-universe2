{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "c44e6ef48a6fd66e8f30032eff60761a4546c792";
  };
}
