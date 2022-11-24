{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    ref = "refs/heads/main";
    rev = "53f503cdcf96be1b366d6c2d1bcb43c89e86527e";
  };
}
