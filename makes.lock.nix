{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "0604c6d611ef8e89c3656749c67d08382c54e73a";
  };
}
