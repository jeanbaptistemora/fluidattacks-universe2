{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "4320b4566479e9ff8c8d38fd76a16f276cef52a1";
  };
}
