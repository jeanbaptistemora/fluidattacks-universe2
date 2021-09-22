{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "068a36c17e4691dc6d78a2b924acfc4a084f6cf5";
  };
}
