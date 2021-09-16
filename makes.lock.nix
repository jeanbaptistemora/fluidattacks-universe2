{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "d268ff40abf12237b1d54987157e17ea6ded2789";
  };
}
