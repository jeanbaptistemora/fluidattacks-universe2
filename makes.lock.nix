{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "446dcd792477149c8cff0bd972607f779878e5b8";
  };
}
