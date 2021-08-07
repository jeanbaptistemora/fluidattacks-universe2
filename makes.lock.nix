{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "cd19ff278b3b7932c4bfa7889e110cf3ff352a33";
  };
}
