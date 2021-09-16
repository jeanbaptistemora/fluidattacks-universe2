{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "e30e69031e5614b50941266547cb07c22fce31fa";
  };
}
