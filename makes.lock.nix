{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "2f18403a393cdebefe0a7bffb6dcb3047583ffc7";
  };
}
