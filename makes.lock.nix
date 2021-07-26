{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "eedeccfe469fb32281eb808d9ab807d864c2020d";
  };
}
