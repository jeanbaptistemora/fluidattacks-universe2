{
  makesSrc = builtins.fetchGit {
    url = "https://github.com/fluidattacks/makes";
    rev = "95f6016c1324985aeff583475849800fac191c94";
  };
}
