{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "b46ed6cebf86017d8e1546738ea2b405e169ff6d";
  };
}
