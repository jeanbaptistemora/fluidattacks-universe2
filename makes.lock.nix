{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "8be37b8178242c65e52bf4d693f61d567e38e712";
  };
}
