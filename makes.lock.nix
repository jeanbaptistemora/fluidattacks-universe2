{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "1593400a20a450887488832451d60605925ca20f";
  };
}
