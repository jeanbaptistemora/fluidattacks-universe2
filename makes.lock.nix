{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "0111fe0b0aed0997287f469aa69894d3ad8ed257";
  };
}
