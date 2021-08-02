{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "ad9de607563acb53ccf752072cf7fb88e8f894cf";
  };
}
