{
  makesSrc = builtins.fetchGit {
    ref = "main";
    url = "https://github.com/fluidattacks/makes";
    rev = "2809ed6bfc466be0496fa8e95c071be188fbddb9";
  };
}
