{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "939a40963d820ad35a296d00cabe43cdce16eae7";
  };
}
