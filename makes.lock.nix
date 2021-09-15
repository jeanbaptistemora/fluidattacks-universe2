{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "ff4ec5797b5c07fe2af35aa75694eef82d55c287";
  };
}
