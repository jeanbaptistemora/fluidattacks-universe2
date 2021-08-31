{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "be905d264a7d029834d03f380f3255add268e3cc";
  };
}
